## POWER MUSIC

**POWER MUSIC** is get a YouTube link to the Korean music site

*Support Music Site*

✔️ **Melon** 

❌ **Bugs** 

❌ **Genie**

## Simple Example Program
It is convert music charts to youtube links with power-music melon.
Youtube link in `id` key
```py
import pm
melon = pm.Controller(time='d',site='melon',song_code='GN0100')
print(melon.get_ytdata())

```
## Melon Music Code Table
- Synthesis

|Catgories|Code|
|:---|:---|
|**Genre**|`GN0000`|
|**Korean**|`DM0000`|
|**Foreign**|`AB0000`|

- Korean Music

|Catgories|Code|
|:---|:---|
|**Ballad**|`GN0100`|
|**Dance**|`GN0200`|
|**Rap/Hip-hop**|`GN0300`|
|**R&B/Soul**|`GN0400`|
|**Indie**|`GN0500`|
|**Rock/Metal**|`GN0600`|
|**Trot**|`GN0700`|
|**Folk/Blues**|`GN0800`|

- Foreign Music

|Catgories|Code|
|:---|:---|
|**POP**|`GN0900`|
|**Rock/Metal**|`GN1000`|
|**Electronica**|`GN1100`|
|**Rap/Hip-hop**|`GN1200`|
|**R&B/Soul**|`GN1300`|
|**Folk/Blues/Country**|`GN1400`|

- Other popular genres

|Catgories|Code|
|:---|:---|
|**OST**|`GN1500`|
|**Jazz**|`GN1700`|
|**Newage**|`GN1800`|
|**J-pop**|`GN1900`|
|**WorldMusic**|`GN2000`|
|**CCM**|`GN2100`|
|**Child/Tae-yying**|`GN2200`|
|**Religious music**|`GN2300`|
|**a-ak; korean music**|`GN2400`|