import re
def linkify_names(df):
    names = df['name'].tolist()
    name_to_abrev = dict(zip(df['name'], df['abrev']))

    for idx, row in df.iterrows():
        for field in ['bio', 'research']:
            text = row.get(field, "")
            if not isinstance(text, str):
                continue

            for name in names:
                if name == row['name']: 
                    continue
                pattern = r'\b' + re.escape(name) + r'\b'
                if re.search(pattern, text):
                    replacement = f"<a href='{name_to_abrev[name]}.html'>{name}</a>"
                    text = re.sub(pattern, replacement, text)
            df.at[idx, field] = text
    return df
