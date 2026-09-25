from collections import deque
from queue import PriorityQueue
import datetime
import json
from .models import Track
from .doubly_linked_list import Playlist

class MediaPlayer:
    def __init__(self):
        self.biblioteca = {}
        self.playlist = Playlist()
        self.up_next = deque()
        self.historico = deque(maxlen=20)

    def carregar_biblioteca(self, arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.biblioteca = {
                item['id']: Track(item['id'], item['title'], item['artist'], item['rating'], item['duration'], item['date_added'])
                for item in dados
            }
        return len(self.biblioteca)

    def listar_biblioteca(self, por="id"):
        chaves = {"rating": lambda t: t.rating, "title": lambda t: t.titulo, "artist": lambda t: t.artista}
        return sorted(self.biblioteca.values(), key=chaves.get(por, lambda t: t.id), reverse=(por == "rating"))

    def _registrar_historico(self, track):
        self.historico.appendleft({
            "track_id": track.id,
            "titulo": track.titulo,
            "artista": track.artista,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })

    def play(self):
        track = self.playlist.current()
        if track:
            self._registrar_historico(track)
            print(f'>>> Tocando: "{track.titulo}" {track.artista} ({track.formatar_duracao()})')
        else:
            print("Nenhuma faixa selecionada.")

    def next_track(self):
        if self.up_next:
            track = self.up_next.popleft()
            self._registrar_historico(track)
            print(f'>>> Tocando: "{track.titulo}" {track.artista} ({track.formatar_duracao()})')
            return

        if self.playlist.play_next():
            self.play()
        else:
            print("Erro: Já está na última música da playlist.")

    def prev_track(self):
        if self.playlist.play_prev():
            self.play()
        else:
            print("Erro: Já está na primeira música da playlist.")

    def enqueue(self, track_id):
        if track_id in self.biblioteca:
            self.up_next.append(self.biblioteca[track_id])
            print(f"Faixa {track_id} adicionada à fila Up Next.")
        else:
            print("Erro: Faixa não encontrada.")

    def smart_shuffle(self, n):
        pq = PriorityQueue()
        for track in self.biblioteca.values():
            pos_hist = next((i for i, h in enumerate(self.historico) if h["track_id"] == track.id), 999)
            penalidade = (5 - pos_hist) if pos_hist < 5 else 10
            prioridade = (-10 * track.rating) + penalidade
            pq.put((prioridade, track.id, track))

        self.playlist = Playlist()
        self.playlist.nome = "Smart Shuffle"
        count = 0
        while not pq.empty() and count < n:
            _, _, track = pq.get()
            self.playlist.adicionar(track)
            count += 1
        print(f"Smart Shuffle gerou nova playlist com {count} faixas.")

    def salvar_estado(self, arquivo):
        estado = {
            "nome_playlist": self.playlist.nome,
            "playlist": [t.to_dict() for t in self.playlist],
            "cursor_id": self.playlist.atual.id if self.playlist.atual else None,
            "up_next": [t.to_dict() for t in self.up_next],
            "historico": list(self.historico)
        }
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(estado, f, ensure_ascii=False, indent=4)
        print(f'Estado salvo em "{arquivo}".')

    def carregar_estado(self, arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            e = json.load(f)

        self.playlist = Playlist()
        self.playlist.nome = e.get("nome_playlist", "")
        for item in e.get("playlist", []):
            self.playlist.adicionar(Track(item['id'], item['title'], item['artist'], item['rating'], item['duration'], item['date_added']))

        self.playlist.reset_cursor()
        while self.playlist.atual and self.playlist.atual.id != e.get("cursor_id"):
            self.playlist.play_next()

        self.up_next = deque([Track(i['id'], i['title'], i['artist'], i['rating'], i['duration'], i['date_added']) for i in e.get("up_next", [])])
        self.historico = deque(e.get("historico", []), maxlen=20)
        print(f'Estado restaurado de "{arquivo}".')