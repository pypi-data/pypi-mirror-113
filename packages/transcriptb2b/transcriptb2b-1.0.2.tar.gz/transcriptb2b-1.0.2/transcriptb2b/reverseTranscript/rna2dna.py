MATCHING_DICTIONARY = {
  'a': 'a',
  'A': 'A',
  'U': 'T',
  'u': 't',
  'c': 'c',
  'C': 'C',
  'g': 'g',
  'G': 'G',
  ' ': ' ',
}

def __transcript_base__(base):
  try:
    return MATCHING_DICTIONARY[base]
  except KeyError:
    return '?'

def reverseT(rna_sequence):
  dna = ''

  for base in rna_sequence:
    dna += __transcript_base__(base)

  return dna
