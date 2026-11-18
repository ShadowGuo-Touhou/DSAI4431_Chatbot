# Spacecraft › Spacecraft Mechanics › Craft Stats › The chaff cloud

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
- Packets drop 8 m below the craft and stay where they were dropped.

- The cloud is one box around all live packets, padded by 10 m.

  - Length = craft speed × 2.25 s + 10 m (2.375 s for High-Coherence).

  - Thickness is at least 10 m. Craft jink while evading, which makes it thicker.

- The cloud is full size from the last packet until 6 s. After 6 s it shrinks from the oldest end. It is gone at 8.25 s (8.375 s for High-Coherence).

- The box is aligned to the map axes, not to the flight path. A trail flown diagonally across the map makes a larger box.

- Its radar return is the area of the box as the radar sees it, times the multiplier. Seen side-on, a cloud returns its length × 10 m. Seen end-on, it returns at least 100 m² (200 m² for High-Coherence).

- Its wake can be seen from all directions. A craft's own wake is strength 1 before modifiers and can only be seen within 75° of its tail.

- It fools active radar, semi-active radar and wake seekers.

- It does nothing against EO (electro-optical), passive radar or home-on-jam seekers. Missiles with an EO validator reject it.

- It is not flagged as a point-defense target, so seekers set to ignore small targets still see it.

- It cannot be shot down.

- Pattern counts refill when the craft is relaunched.

| Craft | Cruise speed | Standard | High-Coherence | The craft itself, side-on |
|---|---|---|---|---|
| RS-35 Halberd | 45 m/s | 1,110 m² | 2,340 m² | 9,900 m² |
| E-44 Sundial | 60 m/s | 1,450 m² | 3,050 m² | 9,900 m² |
| B-45 Sturgeon | 60 m/s | 1,450 m² | 3,050 m² | 6,975 m² |
| B-86 Claymore | 65 m/s | 1,560 m² | 3,290 m² | 2,338 m² |
| PF-386 Barracuda | 100 m/s | 2,350 m² | 4,950 m² | 4,025 m² |
| PF-440 Tanto | 112 m/s | 2,620 m² | 5,520 m² | 1,932 m² |
| RF-286 Pike | 130 m/s | 3,030 m² | 6,380 m² | 2,640 m² |

Cruise speeds are from the spaceframe data. The wiki's craft table lists the Tanto, Barracuda and Pike at 1 m/s faster.
