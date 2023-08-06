"""CosmiX model to deposit charge by high energy ionising particles."""
import os
import logging
import math
import time
from operator import add
from multiprocessing import Pool
import numpy as np
# from tqdm import tqdm
from cosmix.simulation import Simulation
from cosmix.util import read_data
from cosmix.plotting import Plotting


def run_cosmix(detector,
               simulation_mode: str,                    # 'irradiation_beam' / 'cosmic_ray'
               initial_energy: [float, list],           # MeV
               characteristic_length: float,            #
               output_dir: str = 'outputs',             #
               particle_type: str = 'proton',           # 'proton'
               particle_number: int = 10,               # -
               spectrum_file: str = 'data/Gaia_pGCR_201490_NEI_11mm_Al_shielding.tfx.tsv',  # MeV
               starting_position: list = np.array([500., 500., 1.]),   # None,      # um
               beam_direction: list = np.array([0, 0, -1]),      # None,      # -
               random_seed: int = 11111):
    """Simulate charge deposition by cosmic rays.

    :param detector: Pyxel detector object
    :param simulation_mode: simulation mode: ``cosmic_rays``    # ``radioactive_decay``
    :param initial_energy: Kinetic energy of particle in MeV
    :param characteristic_length: in um
    :param output_dir: ``relative/path/to/out/directory``
    :param particle_type: type of particle: ``proton``          # ``alpha``, ``ion``
    :param particle_number: Number of particles
    :param spectrum_file: path to input spectrum in MeV
    :param starting_position: starting position: ``[x, y, z]`` in um
    :param beam_direction: ``[u, v, w]`` unit vector
    :param random_seed: seed
    """
    logging.basicConfig(level=logging.INFO)  # , filename='myapp.log')
    log = logging.getLogger()
    log.info('Started CosmiX')

    if not os.path.isdir(output_dir):
        os.mkdir(str(output_dir))

    if random_seed:
        np.random.seed(random_seed)

    if isinstance(detector, dict):
        det = detector
    else:
        geo = detector.geometry
        mat = detector.material
        det = {
            'det_vert_dimension':   geo.vert_dimension,     # um
            'det_horz_dimension':   geo.horz_dimension,     # um
            'det_total_thickness':  geo.total_thickness,    # um
            'material':             mat.material
        }

    spectrum = None
    if initial_energy == 0. or isinstance(initial_energy, list):

        spectrum = read_data(spectrum_file)                         # x: MeV , y: nuc/m2*s*sr*MeV
        if isinstance(initial_energy, list):
            spectrum_lower_bd = initial_energy[0]       # can be None too
            spectrum_upper_bd = initial_energy[1]       # can be None too
            if spectrum_lower_bd is not None:
                spectrum = spectrum[np.where(spectrum[:, 0] >= spectrum_lower_bd)]
            if spectrum_upper_bd is not None:
                spectrum = spectrum[np.where(spectrum[:, 0] <= spectrum_upper_bd)]

        # TODO: this is not needed now, but needed for other spectra,
        #  depending on the spectrum file content (weigths)

        detector_area = det['det_vert_dimension'] * det['det_horz_dimension'] * 1.0e-8    # cm^2
        spectrum[:, 1] *= 4 * math.pi * 1.0e-4 * detector_area      # x: MeV , y: nuc/s*MeV
        # TODO detector area or detector surface??

        cum_sum = np.cumsum(spectrum[:, 1])
        cum_sum /= np.max(cum_sum)
        spectrum, _ = np.stack((spectrum[:, 0], cum_sum), axis=1), spectrum[:, 1]

    cosmix = Simulation(detector=det,
                        simulation_mode=simulation_mode,
                        char_length=characteristic_length,
                        particle_type=particle_type,
                        initial_energy=initial_energy,
                        spectrum=spectrum,
                        starting_position=starting_position,
                        beam_direction=beam_direction)

    # for k in tqdm(range(0, particle_number)):
    for k in range(0, particle_number):

        e_cluster_size_lst, e_pos0_lst, e_pos1_lst, e_pos2_lst = cosmix.event_generation()

        if isinstance(detector, dict):
            pass
        # within Pyxel:
        else:
            size = len(e_cluster_size_lst)
            detector.charge.add_charge('e',
                                       e_cluster_size_lst,
                                       [0.] * size,
                                       e_pos0_lst, e_pos1_lst, e_pos2_lst,
                                       [0.] * size, [0.] * size, [0.] * size)

        if k % 100 == 0 or k == particle_number - 1:
            np.save(output_dir + '/cosmix_electron_per_event', cosmix.electron_per_event)
            np.save(output_dir + '/cosmix_p_init_energy_lst_per_event', cosmix.p_init_energy_lst_per_event)
            np.save(output_dir + '/cosmix_p_final_energy_lst_per_event', cosmix.p_final_energy_lst_per_event)
            np.save(output_dir + '/cosmix_track_length_lst_per_event', cosmix.track_length_lst_per_event)
            np.save(output_dir + '/cosmix_edep_per_event', cosmix.edep_per_event)
            np.save(output_dir + '/cosmix_step_size_lst_per_step', cosmix.step_size_lst_per_step)

            np.save(output_dir + '/cosmix_angle_alpha_lst_per_event', cosmix.angle_alpha_lst_per_event)
            np.save(output_dir + '/cosmix_angle_beta_lst_per_event', cosmix.angle_beta_lst_per_event)
            np.save(output_dir + '/cosmix_starting_pos_lst_per_event', cosmix.starting_pos_lst_per_event)
            np.save(output_dir + '/cosmix_first_pos_lst_per_event', cosmix.first_pos_lst_per_event)
            np.save(output_dir + '/cosmix_last_pos_lst_per_event', cosmix.last_pos_lst_per_event)
            np.save(output_dir + '/cosmix_direction_lst_per_event', cosmix.direction_lst_per_event)

            np.save(output_dir + '/cosmix_charge_num', cosmix.e_cluster_size_lst)
            np.save(output_dir + '/cosmix_charge_v_pos', cosmix.e_pos0_lst_per_event)
            np.save(output_dir + '/cosmix_charge_h_pos', cosmix.e_pos1_lst_per_event)
            np.save(output_dir + '/cosmix_charge_z_pos', cosmix.e_pos2_lst_per_event)

    # winsound.Beep(440, 2000)
    log.info('Finished')


def run_cosmix_multiprocessing(det=None, mode=None, energy=None, pos=None):
    """TBW."""
    start_time = time.time()

    jobs = 4
    processors = 4
    charlen_list = [2, 10, 2, 10]
    out_list = ['SM_12um/2um', 'SM_12um/10um', 'BAM_35um/2um', 'BAM_35um/10um']

    gaia_bam_ccd = {
        'det_vert_dimension': 45000.,  # um
        'det_horz_dimension': 58980.,  # um
        # 'det_total_thickness': 40.  # um
        'det_total_thickness': 35.  # um
    }
    gaia_sm_ccd = {
        'det_vert_dimension': 45000.,  # um
        'det_horz_dimension': 58980.,  # um
        # 'det_total_thickness': 16.  # um
        'det_total_thickness': 12.  # um
    }
    det_list = [gaia_sm_ccd, gaia_sm_ccd, gaia_bam_ccd, gaia_bam_ccd]
    en_list = [[10., None]] * jobs
    mode_list = ['irradiation_beam'] * jobs
    pos_list = [pos] * jobs
    part_type_list = ['proton'] * jobs
    part_num_list = [10000] * jobs
    spect_list = ['data/proton_L2_solarMin1977_11mm_Shielding.txt'] * jobs

    out_list = list(map(add, len(out_list) * ['outputs/GAIA/'], out_list))
    proc_arg_list = zip(det_list, mode_list, en_list, charlen_list, out_list,
                        part_type_list, part_num_list, spect_list, pos_list)

    with Pool(processes=processors) as pool:
        pool.starmap(run_cosmix, proc_arg_list)

    print('\n\nRunning time: %.3f min' % ((time.time() - start_time) / 60.))


def plotter(det, input_dir):
    """TBW."""

    plots = Plotting(show_plots=True, output_dir='outputs/PLOTS', geometry=det)

    # datafiles = {
    #    '2um, 1000MeV': 'data/stepsize/HgCdTe25/stepsize_2um/stepsize_proton_1000MeV_2um_HgCdTe25_10000_EMopt4.ascii',
    #    '4um, 1000MeV': 'data/stepsize/HgCdTe25/stepsize_4um/stepsize_proton_1000MeV_4um_HgCdTe25_10000_EMopt4.ascii',
    #    '8um, 1000MeV': 'data/stepsize/HgCdTe25/stepsize_8um/stepsize_proton_1000MeV_8um_HgCdTe25_10000_EMopt4.ascii',
    #    # '10um, 11MeV': 'data/stepsize/stepsize_10um/stepsize_proton_11MeV_10um_Si_1000_MicroElec.ascii',
    #    # '10um, 12MeV': 'data/stepsize/stepsize_10um/stepsize_proton_12MeV_10um_Si_1000_MicroElec.ascii',
    #    # '10um, 13MeV': 'data/stepsize/stepsize_10um/stepsize_proton_13MeV_10um_Si_1000_MicroElec.ascii',
    #    # '2um, 9990MeV': 'data/stepsize/stepsize_2um/stepsize_proton_9990MeV_2um_Si_10000_MicroElec.ascii',
    #    # '10um, 9990MeV': 'data/stepsize/stepsize_10um/stepsize_proton_9990MeV_10um_Si_1000_MicroElec.ascii',
    # }
    # plots.check_geant4_distributions(files=datafiles)

    # plots.cluster_positions(chg_v_pos=input_dir + '/cosmix_charge_v_pos.npy',
    #                         chg_h_pos=input_dir + '/cosmix_charge_h_pos.npy',
    #                         chg_z_pos=input_dir + '/cosmix_charge_z_pos.npy')

    # plots.event_tracks_3d(first_pos=input_dir + '/cosmix_first_pos_lst_per_event.npy',
    #                       last_pos=input_dir + '/cosmix_last_pos_lst_per_event.npy')

    # plots.event_polar_angle_dist(alpha=input_dir + '/cosmix_angle_alpha_lst_per_event.npy',
    #                              beta=input_dir + '/cosmix_angle_beta_lst_per_event.npy')

    # plots.event_direction_hist(direction=input_dir + '/cosmix_direction_lst_per_event.npy')

    # plots.event_proton_spectra(
    #     init=input_dir + '/cosmix_p_init_energy_lst_per_event.npy',
    # # # final=input_dir + '/cosmix_p_final_energy_lst_per_event.npy',
    # #     groups='data/stepsize/stepsize_10um/elec_data_library.csv'
    #     groups='data/stepsize/HgCdTe25/stepsize_8um/elec_data_library.csv'
    # )

    # plots.event_starting_position(start_pos=input_dir + '/cosmix_starting_pos_lst_per_event.npy')

    # plots.event_track_length(track=input_dir + '/cosmix_track_length_lst_per_event.npy')

    # plots.event_electrons_deposited(elec=input_dir + '/cosmix_electron_per_event.npy')
    # plots.event_energy_deposited(edep=input_dir + '/cosmix_edep_per_event.npy')
    #
    # plots.cluster_charge_number(chg_num=input_dir + '/cosmix_charge_num.npy')
    # plots.cluster_step_size(step_size=input_dir + '/cosmix_step_size_lst_per_step.npy')

    # s1 = r''
    # s2 = r'$\,\mu m$'
    # elec_dict = {
    #     # s1 + 'SM, $l_{char}=2 ' + s2: 'outputs/GAIA/SM_16um/2um/cosmix_electron_per_event.npy',
    #     # s1 + 'SM, $l_{char}=10' + s2: 'outputs/GAIA/SM_16um/10um/cosmix_electron_per_event.npy',
    #     # s1 + 'BAM, $l_{char}=2 ' + s2: 'outputs/GAIA/run_2um_10MeV_10k_monodir_360grp/cosmix_electron_per_event.npy',
    #     # s1 + 'BAM, $l_{char}=10' + s2: 'outputs/GAIA/run_10um_10MeV_10k_monodir_300grp/cosmix_electron_per_event.npy',
    #     # s1 + 'SM (16' + s2 + '), $l_{char}$=2' + s2: 'outputs/GAIA/SM_16um/2um/cosmix_electron_per_event.npy',
    #     # s1 + 'SM (12' + s2 + '), $l_{char}$=2' + s2: 'outputs/GAIA/SM_12um/2um/cosmix_electron_per_event.npy',
    #     # s1 + 'SM (12' + s2 + '), $l_{char}$=10' + s2: 'outputs/GAIA/SM_12um/10um/cosmix_electron_per_event.npy',
    #     # s1 + 'BAM (40' + s2 + '), $l_{char}$=2' + s2: 'outputs/GAIA/BAM_40um/2um/cosmix_electron_per_event.npy',
    #     # s1 + 'BAM (40' + s2 + '), $l_{char}$=10' + s2: 'outputs/GAIA/BAM_40um/10um/cosmix_electron_per_event.npy',
    #     # s1 + 'BAM (35' + s2 + '), $l_{char}$=2' + s2: 'outputs/GAIA/BAM_35um/2um/cosmix_electron_per_event.npy',
    #     # s1 + 'BAM (35' + s2 + '), $l_{char}$=10' + s2: 'outputs/GAIA/BAM_35um/10um/cosmix_electron_per_event.npy',
    #     # s1 + '10' + s2 + ', isotr.': 'outputs/GAIA/run_10um_10MeV_4k_isotropic_300grp/cosmix_electron_per_event.npy',
    #     # s1+'2 '+s2+', isotropic': 'outputs/GAIA/run_2um_10MeV_4k_isotropic_360grp/cosmix_electron_per_event.npy',
    #     # 'latest': 'outputs/GAIA/cosmix_electron_per_event.npy',
    # }

    plots.plato_histograms()
    plots.plato_particle_contribution()
    #
    plots.gaia_only_data_histograms()
    plots.gaia_bam_histograms()
    plots.gaia_sm_histograms()
    #
    plots.plot_flux_spectrum()

    # # plots.cluster_charges_3d(chg_v_pos=input_dir + '/cosmix_charge_v_pos.npy',
    # #                          chg_h_pos=input_dir + '/cosmix_charge_h_pos.npy',
    # #                          chg_z_pos=input_dir + '/cosmix_charge_z_pos.npy',
    # #                          chg_num=input_dir + '/cosmix_charge_num.npy')
    #

    plots.show()


if __name__ == '__main__':

    plato_ccd = {
        'det_vert_dimension': 1000.,  # um
        'det_horz_dimension': 1000.,  # um
        'det_total_thickness': 15.,   # um
        'material': 'Si'
    }
    # Gaia BAM CCD
    # 4500 × 1966 pixels (parallel × serial)
    # pixel size: 10 × 30 μm
    # vertical dimension (parallel readout direction) = 4500 * 10
    # horizontal dimension (serial readout direction) = 1966 * 30
    gaia_bam_ccd = {
        'det_vert_dimension': 45000.,  # um
        'det_horz_dimension': 58980.,  # um
        'det_total_thickness': 40.,    # um
        'material': 'Si'
    }
    gaia_sm_ccd = {
        'det_vert_dimension': 45000.,  # um
        'det_horz_dimension': 58980.,  # um
        'det_total_thickness': 16.,    # um
        'material': 'Si'
    }

    det, energy, outdir = plato_ccd, 55., 'outputs/PLATO'
    # det, energy, outdir = gaia_bam_ccd, [10., 10000.], 'outputs/GAIA/BAM-10um'
    # det, energy, outdir = gaia_sm_ccd, [10., 10000.], 'outputs/GAIA/SM-10um'
    # det, energy, outdir = gaia_bam_ccd, [10., 10000.], 'outputs/GAIA/BAM-2um'
    # det, energy, outdir = gaia_sm_ccd, [10., 10000.], 'outputs/GAIA/SM-2um'

    mode = 'irradiation_beam'
    pos = [det['det_vert_dimension'] / 2.,
           det['det_horz_dimension'] / 2.,
           1.]
    char_len = 2.
    event_number = 100

    def call():
        run_cosmix(detector=det, simulation_mode=mode, output_dir=outdir,
                   starting_position=pos,
                   initial_energy=energy,
                   characteristic_length=char_len,
                   particle_number=event_number)

    # import timeit
    # num = 1
    # elapsed_time = timeit.timeit(call, number=num) / num
    # print('--- CosmiX ---')
    # print('event number: %d  |  elapsed time (avg): %.3f sec' % (event_number, elapsed_time))

    # plotter(det=det, input_dir='outputs/PLATO')
    # plotter(det=det, input_dir='outputs/GAIA/SM')
    plotter(det=det, input_dir='outputs/GAIA/BAM')
