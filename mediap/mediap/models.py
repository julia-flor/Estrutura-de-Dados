class Track:
    def __init__(self, id, titulo, artista, rating, duracao, data_adicao):
        self.id = int(id)
        self.titulo = str(titulo)
        self.artista = str(artista)
        self.rating = int(rating)
        self.duracao = int(duracao)
        self.data_adicao = str(data_adicao)
        
        # Ponteiros diretos para a Lista Duplamente Encadeada[cite: 1]
        self.proxima = None
        self.anterior = None

    def formatar_duracao(self):
        return f"{self.duracao // 60:02d}:{self.duracao % 60:02d}"

    def to_dict(self):
        return {
            "id": self.id, "title": self.titulo, "artist": self.artista,
            "rating": self.rating, "duration": self.duracao, "date_added": self.data_adicao
        }