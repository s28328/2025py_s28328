from Bio import Entrez,SeqIO
import pandas as pd,matplotlib.pyplot as plt

e=input("Email: ")
k=input("API key: ")
t=input("Taxid: ")
n=input("Min: ")
x=input("Max: ")
Entrez.email,Entrez.api_key=e,k
ids=Entrez.read(Entrez.esearch(db="nucleotide",term=f"txid{t}[Organism:exp] AND {n}:{x}[SLEN]",retmax=100))["IdList"]
d=[]
for i in ids:
 r=SeqIO.read(Entrez.efetch(db="nucleotide",id=i,rettype="gb",retmode="text"),"genbank")
 d.append((r.annotations["accessions"][0],len(r.seq),r.description))
df=pd.DataFrame(d,columns=["accession","length","description"]).sort_values("length",ascending=False)
pre= f"taxid_{t}"
df.to_csv(f"{pre}_report.csv", index=0)
f=plt.figure(figsize=(10,6))
plt.bar(df["accession"],df["length"])
plt.xticks(rotation=90)
plt.xlabel("Accession")
plt.ylabel("Length")
plt.tight_layout()
f.savefig(f"{pre}_plot.png")