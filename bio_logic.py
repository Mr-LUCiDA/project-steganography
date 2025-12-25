import random

class ProteinWatermarker:
    def __init__(self):
        self.codon_table = {
            # --- Standard 20 Asam Amino ---
            'A': 'GCC', 'C': 'TGC', 'D': 'GAC', 'E': 'GAG', 
            'F': 'TTC', 'G': 'GGC', 'H': 'CAC', 'I': 'ATC', 
            'K': 'AAG', 'L': 'CTG', 'M': 'ATG', 'N': 'AAC', 
            'P': 'CCC', 'Q': 'CAG', 'R': 'AGG', 'S': 'AGC', 
            'T': 'ACC', 'V': 'GTG', 'W': 'TGG', 'Y': 'TAC',
            '*': 'TAA',
            
            # --- Karakter Spesial ---
            'U': 'TGA',  
            'O': 'TAG', 
            'J': 'CTG',  
            'B': 'GAC',  
            'Z': 'GAG',  
            'X': 'NNN'
        }
        
    def back_translate(self, protein_seq):
        """Menerjemahkan Protein -> DNA"""
        dna_seq = []
        for aa in protein_seq:
            dna_seq.append(self.codon_table.get(aa, 'NNN'))
        return "".join(dna_seq)

    def inject_scattered(self, host_protein, signature_sentence):
        """
        LOGIKA PENYISIPAN (INSERTION MODE)
        Kata-kata disisipkan DI ANTARA host, memaksa BLAST membuat Gap.
        """
        if not host_protein: return "", "Host kosong."
        clean_host = "".join(host_protein.split()).upper()
        
        if not signature_sentence: return "", "Signature kosong."
        words = signature_sentence.upper().split()
        
        num_inserts = len(words)
        chunk_size = len(clean_host) // (num_inserts + 1)
        
        final_protein_str = ""
        log_info = []
        current_host_idx = 0

        for i, word in enumerate(words):
            variance = random.randint(-2, 2) if chunk_size > 5 else 0
            end_chunk = current_host_idx + chunk_size + variance
            
            if end_chunk > len(clean_host): end_chunk = len(clean_host)
            
            final_protein_str += clean_host[current_host_idx : end_chunk]

            final_protein_str += word
            log_info.append(f"Menyisipkan '{word}' setelah residu ke-{len(final_protein_str)}")
            
            current_host_idx = end_chunk

        final_protein_str += clean_host[current_host_idx:]
        
        final_dna = self.back_translate(final_protein_str)
        
        return final_dna, f"Sukses menyisipkan {len(words)} kata. Total Panjang: {len(final_protein_str)} AA."

    def format_fasta(self, header, sequence):
        header = header if header else "INSERTION_SEQ"
        formatted = f">{header}\n"
        for i in range(0, len(sequence), 80):
            formatted += sequence[i:i+80] + "\n"
        return formatted