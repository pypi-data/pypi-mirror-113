from fetching import Fetching


f = Fetching()
targets = [
    {
        "name": "nthparty/fetching",
        "files": ["fetching/fetching.py"],
        "ref": "055ad6af491f5cd7d308f4fbc5c32852d8748f59"
    }
]

c = f.fetch(targets, "050886f9de266fddeb2ff1b23c8e0b217741942b")
b = f.build(c)
f.write("/Users/ben/Desktop/dev/NTH/fetching/test/fixtures/fetch_single_repo.txt", b)
print("hi")