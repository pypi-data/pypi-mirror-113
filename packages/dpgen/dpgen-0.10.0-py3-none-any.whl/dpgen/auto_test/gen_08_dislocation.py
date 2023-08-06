import os, re, argparse, filecmp, json, glob, math
import subprocess as sp
import numpy as np
import dpgen.auto_test.lib.vasp as vasp
import dpgen.auto_test.lib.lammps as lammps
from pymatgen.core.structure import Structure


global_equi_name = '00.equi'
global_task_name = '08.dislocation'

task_dict={0:'edge',1:'screw'}

def make_vasp(jdata, conf_dir, supercell = [1,1,1]) :
    fp_params = jdata['vasp_params']
    ecut = fp_params['ecut']
    ediff = fp_params['ediff']
    npar = fp_params['npar']
    kpar = fp_params['kpar']
    kspacing = fp_params['kspacing']
    kgamma = fp_params['kgamma']
    
    conf_path = os.path.abspath(conf_dir)
    conf_poscar = os.path.join(conf_path, 'POSCAR')
    # get equi poscar
    equi_path = re.sub('confs', global_equi_name, conf_path)
    equi_path = os.path.join(equi_path, 'vasp-k%.2f' % kspacing)
    equi_contcar = os.path.join(equi_path, 'CONTCAR')
    task_path = re.sub('confs', global_task_name, conf_path)
    task_path = os.path.join(task_path, 'vasp-k%.2f' % kspacing)
    os.makedirs(task_path, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(task_path)
    if os.path.isfile('POSCAR') :
        os.remove('POSCAR')
    os.symlink(os.path.relpath(equi_contcar), 'POSCAR')
    os.chdir(cwd)
    task_poscar = os.path.join(task_path, 'POSCAR')
    # gen structure from equi poscar
    edge = Structure.from_file(task_poscar)
    edge.make_supercell([supercell[0],supercell[1],1])
    center=int(supercell[0]*int(supercell[1]/2)+supercell[0]/2)
    s=[center+supercell[0]*ii for ii in range(int(supercell[1]/2+1))]    
    # gen edge dislocation
    edge.remove_sites(s)
    edge.make_supercell([1,1,supercell[2]])
    # gen screw dislocation
    screw = Structure.from_file(task_poscar)
    screw.make_supercell([supercell[0], supercell[1], supercell[2]],to_unit_cell=False)
    c=[]
    for jj in range(math.ceil(supercell[0]/2)):
        for ii in range(supercell[2]):
            c.append(ii+jj*supercell[2])
    v0 = np.asarray(screw._sites[0].coords, float) - np.asarray(screw._sites[1].coords, float)
    for kk in range(math.ceil(supercell[1]/2)):
        dc=[ii+kk*supercell[0]*supercell[2] for ii in c]
        v=(math.ceil(supercell[1]/2)-kk)/math.ceil(supercell[1]/2)*v0
        screw.translate_sites(dc, vector=v, frac_coords=False, to_unit_cell=False)
    dss = []
    dss.append(edge)
    dss.append(screw)


    # gen incar
    fc = vasp.make_vasp_relax_incar(ecut, ediff, True, True, True, npar, kpar, kspacing = kspacing, kgamma = kgamma)
    with open(os.path.join(task_path, 'INCAR'), 'w') as fp :
        fp.write(fc)
    # gen potcar
    with open(task_poscar,'r') as fp :
        lines = fp.read().split('\n')
        ele_list = lines[5].split()
    potcar_map = jdata['potcar_map']
    potcar_list = []
    for ii in ele_list :
        assert(os.path.exists(potcar_map[ii]))
        potcar_list.append(potcar_map[ii])
    with open(os.path.join(task_path,'POTCAR'), 'w') as outfile:
        for fname in potcar_list:
            with open(fname) as infile:
                outfile.write(infile.read())
    # gen tasks    
    copy_str = "%sx%sx%s" % (supercell[0], supercell[1], supercell[2])
    cwd = os.getcwd()
    for ii in range(len(dss)) :
        struct_path = os.path.join(task_path, 'struct-%s-%s' % (copy_str,task_dict[ii]))
        print('# generate %s' % (struct_path))
        os.makedirs(struct_path, exist_ok=True)
        os.chdir(struct_path)
        for jj in ['POSCAR', 'POTCAR', 'INCAR'] :
            if os.path.isfile(jj):
                os.remove(jj)
        # make conf
        dss[ii].to('POSCAR', 'POSCAR')
        # link incar, potcar, kpoints
        os.symlink(os.path.relpath(os.path.join(task_path, 'INCAR')), 'INCAR')
        os.symlink(os.path.relpath(os.path.join(task_path, 'POTCAR')), 'POTCAR')
        # save supercell
        np.savetxt('supercell.out', supercell, fmt='%d')
    os.chdir(cwd)


def make_lammps(jdata, conf_dir, supercell,task_type) :

    kspacing = jdata['vasp_params']['kspacing']
    fp_params = jdata['lammps_params']
    model_dir = fp_params['model_dir']
    type_map = fp_params['type_map'] 
    model_dir = os.path.abspath(model_dir)
    model_name =fp_params['model_name']
    if not model_name :
        models = glob.glob(os.path.join(model_dir, '*pb'))
        model_name = [os.path.basename(ii) for ii in models]
    else:
        models = [os.path.join(model_dir,ii) for ii in model_name]

    model_param = {'model_name' :      fp_params['model_name'],
                  'param_type':          fp_params['model_param_type']}

    ntypes = len(type_map)

    conf_path = os.path.abspath(conf_dir)
    conf_poscar = os.path.join(conf_path, 'POSCAR')
    # get equi poscar
    equi_path = re.sub('confs', global_equi_name, conf_path)
    equi_path = os.path.join(equi_path, 'vasp-k%.2f' % kspacing)
    equi_contcar = os.path.join(equi_path, 'CONTCAR')
    # equi_path = re.sub('confs', global_equi_name, conf_path)
    # equi_path = os.path.join(equi_path, 'lmp')
    # equi_dump = os.path.join(equi_path, 'dump.relax')
    task_path = re.sub('confs', global_task_name, conf_path)
    task_path = os.path.join(task_path, task_type)
    os.makedirs(task_path, exist_ok=True)
    # gen task poscar
    task_poscar = os.path.join(task_path, 'POSCAR')
    # lammps.poscar_from_last_dump(equi_dump, task_poscar, deepmd_type_map)
    cwd = os.getcwd()
    os.chdir(task_path)
    if os.path.isfile('POSCAR') :
        os.remove('POSCAR')
    os.symlink(os.path.relpath(equi_contcar), 'POSCAR')
    os.chdir(cwd)
    # gen structure from equi poscar
    edge = Structure.from_file(task_poscar)
    edge.make_supercell([supercell[0],supercell[1],1])
    center=int(supercell[0]*int(supercell[1]/2)+supercell[0]/2)
    s=[center+supercell[0]*ii for ii in range(int(supercell[1]/2+1))]
    # gen edge dislocation
    edge.remove_sites(s)
    edge.make_supercell([1,1,supercell[2]])
    # gen screw dislocation
    screw = Structure.from_file(task_poscar)
    screw.make_supercell([supercell[0], supercell[1], supercell[2]],to_unit_cell=False)
    c=[]
    for jj in range(math.ceil(supercell[0]/2)):
        for ii in range(supercell[2]):
            c.append(ii+jj*supercell[2])
    v0 = np.asarray(screw._sites[0].coords, float) - np.asarray(screw._sites[1].coords, float)
    for kk in range(math.ceil(supercell[1]/2)):
        dc=[ii+kk*supercell[0]*supercell[2] for ii in c]
        v=(math.ceil(supercell[1]/2)-kk)/math.ceil(supercell[1]/2)*v0
        screw.translate_sites(dc, vector=v, frac_coords=False, to_unit_cell=False)
    dss = []
    dss.append(edge)
    dss.append(screw)

    # gen tasks    
    cwd = os.getcwd()
    # make lammps.in, relax at 0 bar (scale = 1)
    if task_type=='deepmd':
        fc = lammps.make_lammps_elastic('conf.lmp', 
                                    ntypes, 
                                    lammps.inter_deepmd,
                                    model_name)
    elif task_type =='meam':
        fc = lammps.make_lammps_elastic('conf.lmp', 
                                    ntypes, 
                                    lammps.inter_meam,
                                    model_param) 

    f_lammps_in = os.path.join(task_path, 'lammps.in')
    with open(f_lammps_in, 'w') as fp :
        fp.write(fc)
    # gen tasks    
    copy_str = "%sx%sx%s" % (supercell[0], supercell[1], supercell[2])
    cwd = os.getcwd()
    if task_type=='deepmd':
        os.chdir(task_path)
        for ii in model_name :
            if os.path.exists(ii) :
                os.remove(ii)
        for (ii,jj) in zip(models, model_name) :
            os.symlink(os.path.relpath(ii), jj)
        share_models = glob.glob(os.path.join(task_path, '*pb'))
    else :
        share_models=models

    for ii in range(len(dss)) :
        struct_path = os.path.join(task_path, 'struct-%s-%s' % (copy_str,task_dict[ii]))
        print('# generate %s' % (struct_path))
        os.makedirs(struct_path, exist_ok=True)
        os.chdir(struct_path)
        for jj in ['conf.lmp', 'lammps.in'] + model_name :
            if os.path.isfile(jj):
                os.remove(jj)
        # make conf
        dss[ii].to('POSCAR', 'POSCAR')
        lammps.cvt_lammps_conf('POSCAR', 'conf.lmp')
        ptypes = vasp.get_poscar_types('POSCAR')
        lammps.apply_type_map('conf.lmp', type_map, ptypes)    
        # link lammps.in
        os.symlink(os.path.relpath(f_lammps_in), 'lammps.in')
        # link models
        for (ii,jj) in zip(share_models, model_name) :
            os.symlink(os.path.relpath(ii), jj)
        # save supercell
        np.savetxt('supercell.out', supercell, fmt='%d')
    os.chdir(cwd)

def _main() :
    parser = argparse.ArgumentParser(
        description="gen 08.dislocation")
    parser.add_argument('TASK', type=str,
                        help='the task of generation, vasp or lammps')
    parser.add_argument('PARAM', type=str,
                        help='json parameter file')
    parser.add_argument('CONF', type=str,
                        help='the path to conf')
    parser.add_argument('COPY', type=int, nargs = 3,
                        help='the path to conf')
    args = parser.parse_args()

    with open (args.PARAM, 'r') as fp :
        jdata = json.load (fp)

#    print('# generate %s task with conf %s' % (args.TASK, args.CONF))
    if args.TASK == 'vasp':
        make_vasp(jdata, args.CONF, args.COPY)
    elif args.TASK == 'deepmd' or args.TASK == 'meam' :
        make_lammps(jdata, args.CONF, args.COPY, args.TASK)
    #elif args.TASK == 'meam' :
    #    make_meam_lammps(jdata, args.CONF, args.COPY)
    else :
        raise RuntimeError("unknow task ", args.TASK)
    
if __name__ == '__main__' :
    _main()
