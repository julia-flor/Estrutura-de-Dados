from .player import MediaPlayer
from .doubly_linked_list import Playlist

def run_cli():
    player = MediaPlayer()

    while True:
        try:
            partes = input("mediap> ").strip().split()
        except (KeyboardInterrupt, EOFError):
            break

        if not partes:
            continue

        cmd = partes[0].lower()

        if cmd == "quit":
            break
        elif cmd == "library":
            if len(partes) >= 3 and partes[1] == "load":
                print(f"Biblioteca carregada: {player.carregar_biblioteca(partes[2])} faixas.")
            elif len(partes) >= 2 and partes[1] == "list":
                por = partes[partes.index("--by") + 1] if "--by" in partes else "id"
                for t in player.listar_biblioteca(por):
                    print(f"{t.id}. {t.titulo} - {t.artista} ({t.formatar_duracao()}) [{t.rating}★]")
        elif cmd == "playlist":
            sub = partes[1] if len(partes) > 1 else ""
            if sub == "new" and len(partes) >= 3:
                player.playlist = Playlist()
                player.playlist.nome = partes[2]
                print(f'Playlist "{partes[2]}" criada.')
            elif sub == "add" and len(partes) >= 3:
                tid = int(partes[2])
                if tid in player.biblioteca:
                    player.playlist.adicionar(player.biblioteca[tid])
                    print(f"Faixa {tid} adicionada.")
            elif sub == "remove" and len(partes) >= 3:
                print("Removido." if player.playlist.remover_na_posicao(int(partes[2])) else "Posição inválida.")
            elif sub == "show":
                atual = player.playlist.current()
                for idx, t in enumerate(player.playlist, 1):
                    print(f"{'>' if t == atual else ' '} {idx}. {t.titulo} {t.artista} ({t.formatar_duracao()})")
        elif cmd == "play":
            player.play()
        elif cmd == "next":
            player.next_track()
        elif cmd == "prev":
            player.prev_track()
        elif cmd == "enqueue" and len(partes) >= 2:
            player.enqueue(int(partes[1]))
        elif cmd == "queue" and len(partes) >= 2 and partes[1] == "show":
            for idx, t in enumerate(player.up_next, 1):
                print(f"{idx}. {t.titulo} - {t.artista}")
        elif cmd == "history":
            for idx, item in enumerate(player.historico, 1):
                print(f"{idx}. {item['titulo']} {item['artista']} [{item['timestamp']}]")
        elif cmd == "smart-shuffle" and len(partes) >= 2:
            player.smart_shuffle(int(partes[1]))
        elif cmd == "save" and len(partes) >= 2:
            player.salvar_estado(partes[1])
        elif cmd == "load" and len(partes) >= 2:
            player.carregar_estado(partes[1])
        else:
            print("Comando desconhecido.")