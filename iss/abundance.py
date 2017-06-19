#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import os
import sys
import logging


def parse_abundance_file(abundance_file):
    """Parse an abundance file

    The abundance file is a flat file of the format "genome_id<TAB>abundance"

    Args:
        abundance_file (string): the path to the abundance file

    Returns:
        abundance_dic (dict): dict with genome_id as keys, abundance as
            values
    """
    logger = logging.getLogger(__name__)
    abundance_dic = {}
    try:
        assert os.stat(abundance_file).st_size != 0
        f = open(abundance_file, 'r')
    except IOError as e:
        logger.error('Failed to open abundance file:%s' % e)
        sys.exit(1)
    except AssertionError as e:
        logger.error('Abundance file seems empty: %s' % abundance_file)
        sys.exit(1)
    else:
        with f:
            for line in f:
                try:
                    genome_id = line.split()[0]
                    abundance = float(line.split()[1])
                except IndexError as e:
                    logger.error('Failed to read abundance file: %s' % e)
                else:
                    abundance_dic[genome_id] = abundance
    logger.info('Loaded abundance file: %s' % abundance_file)
    return abundance_dic


def to_coverage(total_n_reads, species_abundance, read_length, genome_size):
    """Calculate the coverage of a genome in a metagenome given its size and
    abundance

    Args:
        total_n_reads (int): total amount of reads in the dataset
        species_abundance (float): abundance of the species, between 0 and 1
        read_length (int): length of the reads in the dataset
        genome_size (int): size of the genome

    Returns:
        coverage (float): genome coverage
    """
    n_reads = total_n_reads * species_abundance
    coverage = (n_reads * read_length) / genome_size
    return coverage
