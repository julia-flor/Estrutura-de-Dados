class Playlist:
    def __init__(self):
        self.nome = ""
        self.primeira = None
        self.ultima = None
        self.atual = None  # Cursor da playlist[cite: 1]
        self.tamanho = 0

    def adicionar(self, track):
        """Adiciona uma faixa ao final[cite: 1]"""
        if not self.primeira:
            self.primeira = self.ultima = self.atual = track
        else:
            self.ultima.proxima = track
            track.anterior = self.ultima
            self.ultima = track
        self.tamanho += 1

    def remover_na_posicao(self, pos):
        """Remove a faixa na posição pos (1-based)[cite: 1]"""
        if pos < 1 or pos > self.tamanho:
            return False

        no = self.primeira
        for _ in range(pos - 1):
            no = no.proxima

        if no == self.atual:
            self.atual = no.proxima or no.anterior

        if no.anterior:
            no.anterior.proxima = no.proxima
        else:
            self.primeira = no.proxima

        if no.proxima:
            no.proxima.anterior = no.anterior
        else:
            self.ultima = no.anterior

        self.tamanho -= 1
        return True

    def current(self):
        return self.atual

    def play_next(self):
        if self.atual and self.atual.proxima:
            self.atual = self.atual.proxima
            return True
        return False

    def play_prev(self):
        if self.atual and self.atual.anterior:
            self.atual = self.atual.anterior
            return True
        return False

    def reset_cursor(self):
        self.atual = self.primeira

    def __len__(self):
        return self.tamanho

    def __iter__(self):
        atual = self.primeira
        while atual:
            yield atual
            atual = atual.proxima