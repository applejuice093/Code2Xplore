"""Day 9: show how aliasing, shallow copies and deep copies differ for nested data."""
import copy

def generate_data():
    """Return a fresh nested dataset: a list of records with inner dicts and file lists."""
    dataset = [
        {"id": 1, 
        "data": {"files": ["a.txt", "b.txt"], "usage": 500}
        },
        {"id": 2,
        "data": {"files": ["c.txt", "d.txt"], "usage": 300}
        }
    ]
    return dataset

def replicate_data(root_db):
    """Return (alias, shallow copy, deep copy) of root_db.

    The alias is the same object, the shallow copy is a new outer list that still
    shares the inner dicts/lists, and the deep copy shares nothing.
    """
    alias_db = root_db
    shallow_db = copy.copy(root_db)
    deep_db = copy.deepcopy(root_db)
    return alias_db, shallow_db, deep_db

def modify_data(root, a_db, s_db, d_db, dev, roll):
    """Mutate each copy in place to show which changes leak back into root.

    An odd roll number drops the last file of the first shallow record, an even
    one appends a new file. Returns the four datasets unchanged in identity.
    """
    a_db[0]["id"] = 101
    
    s_db.append({
        "id": 3,
        "data": {"files": [f"log_{dev}.txt"], "usage": 100}
    })
    
    if roll % 2 != 0:
        if len(s_db[0]["data"]["files"]) > 0:
            dropped = s_db[0]["data"]["files"].pop()
            print(f"\n{dev}'s logic triggered -> Roll {roll} is ODD. Deleted: {dropped}")
    else:
        s_db[0]["data"]["files"].append(f"newfile_{roll}.txt")
        print(f"\n{dev}'s logic triggered -> Roll {roll} is EVEN. Added new file.")
        
    s_db[1]["data"]["usage"] = roll * 2
    
    d_db[0]["data"]["usage"] = 0
    if len(d_db[1]["data"]["files"]) > 0:
        d_db[1]["data"]["files"].pop()
        
    return root, a_db, s_db, d_db

def check_integrity(pure_db, current_root, s_copy):
    """Compare current_root against an untouched snapshot (pure_db).

    Returns (leaked records, secure records, number of file names shared by
    current_root and the shallow copy).
    """
    leak_flags = 0
    secure_flags = 0
    
    for i in range(len(pure_db)):
        if pure_db[i] != current_root[i]:
            leak_flags += 1
            print(f"WARNING: Corruption at ID {pure_db[i]['id']}")
        else:
            secure_flags += 1

    root_files = set()
    for item in current_root:
        root_files.update(item.get("data", {}).get("files", []))
        
    s_files = set()
    for item in s_copy:
        s_files.update(item.get("data", {}).get("files", []))
        
    overlap_set = root_files.intersection(s_files)
    overlap_count = len(overlap_set)
    
    print("\nCorruption occurs if modifications on the copy impact the original unintentionally.")
    print("Elements inside shallow copies will be modified concurrently since Python only performs the copying of the topmost layer of list.")
    print("Memory references to inner dictionaries and lists remain the same.")
    
    return (leak_flags, secure_flags, overlap_count)

def main():
    """Run the demo: replicate, modify, then print the integrity report."""
    my_name = "Aniket"
    my_roll = 11701
    
    print(f"--- Multi-Level Data Analyzer | {my_name} | {my_roll} ---")
    
    db_original = generate_data()
    db_snapshot = copy.deepcopy(db_original)
    
    print(f"\nSTARTING DATA:\n{db_original}")
    
    db_alias, db_shallow, db_deep = replicate_data(db_original)
    
    db_original, db_alias, db_shallow, db_deep = modify_data(
        db_original, db_alias, db_shallow, db_deep, my_name, my_roll
    )
    
    print("\nDisplay:")
    print(" original data:")
    print(f"  {db_original}")
    print(" shallow copy result:")
    print(f"  {db_shallow}")
    print(" deep copy result:")
    print(f"  {db_deep}")
    print(" integrity report:")
    final_metrics = check_integrity(db_snapshot, db_original, db_shallow)
    print(f" tuple -> {final_metrics}")

if __name__ == "__main__":
    main()
