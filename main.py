import json
import random

from classes import *


pygame.init()

player_speed = 4
player_texture_scale = 0.25
camera_lag = 10


def main():
    with open("textures.json", "r") as f:
        texture_dictionary = json.load(f)

    w = pygame.display.set_mode((1600, 900))
    player = Player(w, texture_dictionary["Player"], player_speed, player_texture_scale)
    world = World(w, player, camera_lag)
    # render_test_assets(w, world, texture_dictionary)

    add_intro_slide(w, world, texture_dictionary)
    add_all_text(w, world, texture_dictionary)

    c = pygame.time.Clock()
    elapsed_time_ms = c.tick(60)

    meowing = True
    while meowing:
        # print("new frame")
        all_events = pygame.event.get()
        all_keys = pygame.key.get_pressed()
        for event in all_events:
            if event.type == pygame.QUIT:
                meowing = False
        world.update_world(all_events, all_keys, elapsed_time_ms)

        # print(player.position)
        # print(player.image_file)
        w.fill((0, 0, 0))
        world.draw_world(elapsed_time_ms)
        pygame.display.flip()
        elapsed_time_ms = c.tick(60)


def add_intro_slide(w, world, texture_dictionary):
    world.world_objects.append(WorldObjectText(
        w, [-w.get_width() / 4, -w.get_height() / 4],
        8,
        "にほんごのプレゼンテイション！！！！！！！",
        "Choco Cooky",
        40,
        (255, 0, 255)
    ))

    world.world_objects.append(WorldObjectVideo(
        w, [-w.get_width() / 4, -w.get_height() / 4 + 100],
        texture_dictionary["OsakaWaveGif"],
        6,
        texture_scale=0.75,
        loop=True,
        paused=False
    ))
    world.world_objects.append(WorldObjectVideo(
        w, [-w.get_width() / 4 + 400, -w.get_height() / 4 + 100],
        texture_dictionary["TomoPointRightGif"],
        6,
        texture_scale=0.75,
        loop=True,
        paused=False
    ))


def add_all_text(w, world, texture_dictionary):
    sentences = """みんなさんこんにちわ！
    なにがあずまんがだいおうですか？
    あずまんがだいおうはアニメのコメディです。
    J。C。Staffはにせんさんねんにあずまんがだいおうをつくりました
    まいにちあずまんがだいおうをみます。
    あずまんがだいおうとおさかさんがだいすきです。
    おさかさんとともだちはにほんでがっこうにいきます。
    しゅうまつにおさかさんはがっこうにいきません。
    おさかさんはたのしいです。かぐらさんとともさんもたのしいです。
    おさかさんとあいたいです。
    おさかさんはサーターアンダーギーをたべました。
    サーターアンダーギーはおいしいです。
    おさかさんはサーターアンダーギーをはなしました。
    おさかさんはサーターアンダーギーがだいすきです。
    さかきさんはかわいいです。
    よみさんはまじめです。
    ともさんはうるさいです。
    さかきさんとともさんとよみさんとちよちゃんとかおりんさんとかぐらさんはおさかさんのともだちです。
    ちよちゃんはじゅうさいです。
    ちよちゃんがすきじゃないです。
    わたしはちよちゃんをたべました。
    ちよちゃんはまずいです。
    いっしょにつくりませんか？
    いいですね！つくりましょう！
    しつもんがありますか？"""

    font_size = 36
    sentence_spacing = 1200

    m = 0
    for i in sentences.split("\n"):
        special_offset = 0
        m += 1
        if m == 18:
            special_offset = -400
        world.world_objects.append(WorldObjectText(
            w, [sentence_spacing * m + special_offset, -w.get_height() / 4],
            8,
            i,
            "Choco Cooky",
            font_size,
            (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        ))
        match m:
            case 1:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 200],
                    texture_dictionary["AmericaYaVideo"],
                    7,
                    audio_path=texture_dictionary["AmericaYaAudio"],
                    texture_scale=0.75,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 2:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["ChiyoThinkGif"],
                    6,
                    texture_scale=0.75,
                    loop=True,
                    paused=False
                ))
            case 3:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 100],
                    texture_dictionary["OsakaScary"],
                    5
                ))
            case 4:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["JCStaffLogo"],
                    5,
                    texture_scale=0.25
                ))
            case 5:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["ChiyoGibberishGif"],
                    6,
                    texture_scale=0.75,
                    paused=False
                ))
            case 6:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m - 100, -w.get_height() / 4 + 100],
                    texture_dictionary["OsakaWater"],
                    5,
                    texture_scale=0.75
                ))
            case 7:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["OsakaGangSigns"],
                    5,
                    texture_scale=0.75
                ))
            case 8:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["OsakaCasino"],
                    5,
                    texture_scale=0.75
                ))
            case 9:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["OsakaTerrorism"],
                    5,
                    texture_scale=0.75
                ))
            case 10:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["OsakaDate"],
                    5,
                    texture_scale=0.75
                ))
            case 11:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 200],
                    texture_dictionary["OsakaSataAndagiVideo"],
                    7,
                    audio_path=texture_dictionary["OsakaSataAndagiAudio"],
                    texture_scale=0.50,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 12:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 200],
                    texture_dictionary["OsakaSataAndagiSoundEffectVideo"],
                    7,
                    audio_path=texture_dictionary["OsakaSataAndagiSoundEffectAudio"],
                    texture_scale=0.50,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 13:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 200],
                    texture_dictionary["OsakaSataAndagiSoundEffectVideo"],
                    7,
                    audio_path=texture_dictionary["OsakaSataAndagiSoundEffectAudio"],
                    texture_scale=0.50,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 14:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 200],
                    texture_dictionary["OsakaSataAndagiSoundEffectVideo"],
                    7,
                    audio_path=texture_dictionary["OsakaSataAndagiSoundEffectAudio"],
                    texture_scale=0.50,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 15:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 200],
                    texture_dictionary["SakakiCatVideo"],
                    7,
                    audio_path=texture_dictionary["SakakiCatAudio"],
                    texture_scale=2,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 16:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["YomiNerd"],
                    5,
                    texture_scale=0.75
                ))
            case 17:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m - 200, -w.get_height() / 4 + 200],
                    texture_dictionary["TomoSubwayVideo"],
                    7,
                    audio_path=texture_dictionary["TomoSubwayAudio"],
                    texture_scale=1,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 18:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["AzumangaGang"],
                    5,
                    texture_scale=0.75
                ))
            case 19:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 200],
                    texture_dictionary["ChiyoJumpVideo"],
                    7,
                    audio_path=texture_dictionary["ChiyoJumpAudio"],
                    texture_scale=0.75,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 20:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["ChiyoNoahArk"],
                    5,
                    texture_scale=0.75
                ))
            case 21:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 200],
                    texture_dictionary["ChiyoBreadVideo"],
                    7,
                    audio_path=texture_dictionary["ChiyoBreadAudio"],
                    texture_scale=1,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 22:
                world.world_objects.append(WorldObjectSprite(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 100],
                    texture_dictionary["ChiyoGrind"],
                    5,
                    texture_scale=0.75
                ))
            case 23:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 200],
                    texture_dictionary["ChiyoTsukurimashouBadEndVideo"],
                    7,
                    audio_path=texture_dictionary["ChiyoTsukurimashouBadEndAudio"],
                    texture_scale=1,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 24:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 200],
                    texture_dictionary["ChiyoTsukurimashouDrakeVideo"],
                    7,
                    audio_path=texture_dictionary["ChiyoTsukurimashouDrakeAudio"],
                    texture_scale=1,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))
            case 25:
                world.world_objects.append(WorldObjectVideo(
                    w, [sentence_spacing * m, -w.get_height() / 4 + 200],
                    texture_dictionary["ChiyoMeatballsVideo"],
                    7,
                    audio_path=texture_dictionary["ChiyoMeatballsAudio"],
                    texture_scale=2,
                    play_icon_path=texture_dictionary["PlayIcon"]
                ))


def render_test_assets(w, world, texture_dictionary):
    world.world_objects.append(WorldObjectSprite(w, [100, 100], texture_dictionary["RikaChan"], 5))
    world.world_objects.append(WorldObjectVideo(
        w, [200, 100],
        texture_dictionary["CatRappingVideo"],
        6,
        audio_path=texture_dictionary["CatRappingAudio"],
        texture_scale=0.25,
        play_icon_path=texture_dictionary["PlayIcon"]
    ))
    world.world_objects.append(WorldObjectVideo(
        w, [200, 800],
        texture_dictionary["SillyVideo"],
        7,
        audio_path=texture_dictionary["SillyAudio"],
        texture_scale=0.5,
        play_icon_path=texture_dictionary["PlayIcon"]
    ))
    world.world_objects.append(WorldObjectText(
        w, [200, 400],
        8,
        "i love osaka gaming",
        "Choco Cooky",
        16,
        (255, 0, 255)
    ))


if __name__ == "__main__":
    main()

