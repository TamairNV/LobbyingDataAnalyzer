import re
def extract_bill_codes(text):
    # This pattern looks for:
    # 1. The Prefix (H.R., S., H.J.Res, etc.) with optional dots and spaces
    # 2. The Number (digits)
    # 3. Flexible spacing in between

    pattern = r'''
        \b                      # Start at a word boundary
        (                       # Start Group 1: The Prefix
            H\.?R\.?          | # Matches H.R., HR, H. R.
            S\.?              | # Matches S., S
            H\.?J\.?Res\.?    | # House Joint Resolutions
            S\.?J\.?Res\.?    | # Senate Joint Resolutions
            H\.?Res\.?        | # House Resolutions
            S\.?Res\.?        | # Senate Resolutions
            P\.?L\.?          | # Public Laws (P.L.)
            Senate\s+Bill       # "Senate Bill" written out
        )
        \s* # Optional whitespace (handles "H.R.123" vs "H.R. 123")
        \.?                     # Optional extra dot (for messy typos)
        \s* # More optional whitespace
        (\d+(?:-\d+)?)          # Group 2: The Number (allows "123" or "117-10")
        \b                      # End at a word boundary
    '''

    # re.VERBOSE allows us to write the regex with comments and whitespace for readability
    matches = re.findall(pattern, text, re.IGNORECASE | re.VERBOSE)

    # Clean and standardize results
    cleaned_bills = []
    for prefix, number in matches:
        # Standardize the prefix to a clean format (e.g., "HR" -> "H.R.")
        clean_prefix = normalize_prefix(prefix)
        cleaned_bills.append(f"{clean_prefix} {number}")

    return list(set(cleaned_bills))  # Return unique items only


def normalize_prefix(raw_prefix):
    """Standardizes messy prefixes into API-friendly formats"""
    raw = raw_prefix.upper().replace('.', '').replace(' ', '')

    if 'HR' in raw: return "H.R."
    if 'SJRES' in raw: return "S.J.Res."
    if 'HJRES' in raw: return "H.J.Res."
    if 'SRES' in raw: return "S.Res."
    if 'HRES' in raw: return "H.Res."
    if 'PL' in raw: return "P.L."
    if raw == 'S' or 'SENATE' in raw: return "S."
    return raw_prefix  # Fallback