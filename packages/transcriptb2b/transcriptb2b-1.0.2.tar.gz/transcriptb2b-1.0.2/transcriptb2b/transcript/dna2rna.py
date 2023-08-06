MATCHING_DICTIONARY = {
  'a': 'a',
  'A': 'A',
  'T': 'U',
  't': 'u',
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

def transcript(dna_sequence):
  rna = ''

  for base in dna_sequence:
    rna += __transcript_base__(base)

  return rna
