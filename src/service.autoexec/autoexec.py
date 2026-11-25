import os
import re
import xbmc
import xbmcvfs

SKIN_ID = "skin.ker0n3.flix"
XML_PATH = xbmcvfs.translatePath(f"special://home/addons/{SKIN_ID}/xml/Includes_Flix.xml")
INICIO_XML_PATH = xbmcvfs.translatePath(f"special://home/addons/{SKIN_ID}/xml/FlixInicio.xml")
MARKER = "<!-- PATCH_YOSEBA_V52_SINOPSIS_RECORTADA_OK -->"
INICIO_MARKER = "<!-- PATCH_YOSEBA_INICIO_TOP10_V38_OK -->"


def log(msg):
    xbmc.log(f"[service.autoexec] {msg}", xbmc.LOGINFO)


def replace_include_block(content, include_name, transform_fn):
    start_tag = f'<include name="{include_name}">'
    start_idx = content.find(start_tag)
    if start_idx == -1:
        log(f"No se encontró {start_tag}")
        return content
    m_end = re.search(r'\r?\n\t</include>', content[start_idx:])
    if not m_end:
        log(f"No se encontró cierre </include> para {include_name}")
        return content
    end_idx = start_idx + m_end.end()
    block = content[start_idx:end_idx]
    new_block = transform_fn(block)
    return content[:start_idx] + new_block + content[end_idx:]


def patch_flix_xml():
    changed = False

    if os.path.exists(XML_PATH):
        with open(XML_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        if MARKER not in content:
            for old_m in (
                "<!-- PATCH_YOSEBA_V51_OK -->",
                "<!-- PATCH_YOSEBA_V20_PROPORCION_IZQUIERDA_OK -->",
                "<!-- PATCH_YOSEBA_V19_PUSH_DERECHA_OK -->",
                "<!-- PATCH_YOSEBA_V18_ZOOM_EPISODIOS_OK -->",
                "<!-- PATCH_YOSEBA_V17_POSTER_OCULTO_OK -->",
                "<!-- PATCH_YOSEBA_V16_APAISADO_MAS_GRANDE_OK -->",
                "<!-- PATCH_YOSEBA_V15_BORDE_APAISADO_OK -->",
                "<!-- PATCH_YOSEBA_V14_APAISADO_EXACTO_OK -->",
                "<!-- PATCH_YOSEBA_V13_APAISADO_ALTURA_OK -->",
                "<!-- PATCH_YOSEBA_V12_APAISADO_LIMPIO_OK -->",
                "<!-- PATCH_YOSEBA_V11_APAISADO_OK -->",
                "<!-- PATCH_YOSEBA_V10_TOP10_COMPACT_OK -->",
                "<!-- PATCH_YOSEBA_V9_TOP10_OK -->",
                "<!-- PATCH_YOSEBA_V8_ZOOM_SUAVE_OK -->",
                "<!-- PATCH_YOSEBA_V7_ACTUALIZADO_OK -->",
            ):
                content = content.replace(old_m + "\r\n", "").replace(old_m + "\n", "").replace(old_m, "")

            newline = "\r\n" if "\r\n" in content else "\n"
            original = content

            def patch_menu_preview(blk):
                pat = (
                    r'(<control type="group">\s*<left>350</left>\s*)<top>438</top>'
                    r'(\s*<include content="FlixMenuPreviewRow">.*?</include>)\s*'
                    r'(<include content="FlixMenuPreviewRow">.*?</include>)'
                )
                rep = (
                    r'\1<top>620</top>\2' + newline +
                    r'\t\t\t\t<control type="group">' + newline +
                    r'\t\t\t\t\t<visible>false</visible>' + newline +
                    r'\t\t\t\t\t\3' + newline +
                    r'\t\t\t\t</control>'
                )
                return re.sub(pat, rep, blk, count=1, flags=re.DOTALL)

            content = replace_include_block(content, "FlixMenuPreview", patch_menu_preview)

            def patch_menu_preview_row(blk):
                blk = blk.replace('<height>316</height>', '<height>450</height>', 1)
                return re.sub(
                    r'(<control type="list" id="\$PARAM\[list_id\]">\s*<left>0</left>\s*)<top>40</top>(\s*<width>1800</width>\s*)<height>276</height>',
                    r'\1<top>38</top>\2<height>405</height>',
                    blk,
                    count=1
                )

            content = replace_include_block(content, "FlixMenuPreviewRow", patch_menu_preview_row)

            def patch_poster_overlay(blk):
                blk = blk.replace('<param name="px">12</param>', '<param name="px">18</param>')
                blk = re.sub(r'<top>12</top>\s*<width>168</width>\s*<height>252</height>', '<top>10</top>\n\t\t\t<width>244</width>\n\t\t\t<height>366</height>', blk)
                blk = re.sub(r'<top>247</top>\s*<width>150</width>', '<top>378</top>\n\t\t\t\t<width>226</width>', blk)
                blk = re.sub(r'<top>250</top>\s*<width>144</width>', '<top>381</top>\n\t\t\t\t<width>220</width>', blk)
                blk = blk.replace('<param name="dx" value="128" />', '<param name="dx" value="200" />')
                blk = re.sub(r'<left>128</left>\s*<top>212</top>', '<left>204</left>\n\t\t\t\t<top>326</top>', blk)
                blk = re.sub(r'<left>116</left>\s*<top>212</top>', '<left>192</left>\n\t\t\t\t<top>326</top>', blk)
                return blk

            content = replace_include_block(content, "FlixPosterOverlay", patch_poster_overlay)

            def patch_row_static(blk):
                blk = blk.replace('<param name="itemw">192</param>', '<param name="itemw">280</param>')
                blk = blk.replace('<param name="px">12</param>', '<param name="px">18</param>')
                blk = blk.replace('<param name="fx">6</param>', '<param name="fx">12</param>')
                blk = blk.replace('<height>316</height>', '<height>632</height>', 1)
                blk = blk.replace('<left>40</left>', '<left>12</left>', 1)
                blk = re.sub(r'<left>20</left>(\s*)<top>0</top>', '<left>48</left>\1<top>195</top>', blk, count=1)
                blk = re.sub(
                    r'<left>-40</left>(\s*)<top>-16</top>(\s*)<width>1880</width>(\s*)<height>340</height>',
                    '<left>-12</left>\1<top>179</top>\2<width>1908</width>\3<height>440</height>',
                    blk,
                    count=1
                )
                blk = blk.replace('<param name="lh" value="340" />', '<param name="lh" value="440" />')
                blk = re.sub(r'<param name="zoom" value="(?:115|108)" />', '<param name="zoom" value="104" />', blk)
                blk = re.sub(r'<param name="zoomw" value="(?:115|108)" />', '<param name="zoomw" value="104" />', blk)
                blk = re.sub(r'<param name="lift" value="(?:10|0)" />', '<param name="lift" value="4" />', blk)
                blk = blk.replace('<param name="card" value="true" />', '<param name="card" value="false" />')
                return blk

            content = replace_include_block(content, "FlixRowStatic", patch_row_static)

            def patch_row_layouts(blk):
                blk = blk.replace('<param name="itemw">192</param>', '<param name="itemw">280</param>')
                blk = blk.replace('<param name="px">12</param>', '<param name="px">18</param>')
                blk = blk.replace('<param name="fx">6</param>', '<param name="fx">12</param>')
                blk = blk.replace('<param name="lh">276</param>', '<param name="lh">410</param>')
                blk = blk.replace('<param name="zoom">108</param>', '<param name="zoom">104</param>')
                blk = blk.replace('<param name="zoomw">112</param>', '<param name="zoomw">105</param>')
                blk = blk.replace('<param name="push">305</param>', '<param name="push">340</param>')
                blk = re.sub(
                    r'<left>\$PARAM\[px\]</left>(\s*)<top>12</top>(\s*)<width>168</width>(\s*)<height>252</height>',
                    r'<left>$PARAM[px]</left>\1<top>10</top>\2<width>244</width>\3<height>366</height>',
                    blk
                )
                blk = re.sub(
                    r'<left>\$PARAM\[fx\]</left>(\s*)<top>6</top>(\s*)<width>180</width>(\s*)<height>264</height>(\s*)<texture colordiffuse="\$VAR\[FlixAccentW\]">flix/frame_180x264\.png</texture>',
                    r'<left>$PARAM[fx]</left>\1<top>4</top>\2<width>256</width>\3<height>378</height>\4<texture border="24" colordiffuse="$VAR[FlixAccentW]">flix/focus_border.png</texture>',
                    blk
                )
                blk = re.sub(
                    r'<left>0</left>(\s*)<top>190</top>(\s*)<width>74</width>(\s*)<height>74</height>',
                    r'<left>4</left>\1<top>305</top>\2<width>76</width>\3<height>76</height>',
                    blk
                )

                apaisado_cond = "$PARAM[card] + Control.HasFocus($PARAM[list_id]) + System.IdleTime(2) + !String.IsEmpty(ListItem.Art(fanart))"
                c_pos_pre = blk.find("<!-- C (Carlos")
                fl_pos = blk.rfind('<focusedlayout width="$PARAM[itemw]" height="$PARAM[lh]">', 0, c_pos_pre if c_pos_pre != -1 else len(blk))
                if fl_pos != -1:
                    outer_grp = blk.find('<control type="group"><left>$PARAM[ox]</left><top>$PARAM[oy]</top>', fl_pos)
                    if outer_grp != -1:
                        inner_grp = blk.find('<control type="group">', outer_grp + 20)
                        if inner_grp != -1:
                            blk = blk[:inner_grp] + f'<control type="group"><visible>![{apaisado_cond}]</visible>' + blk[inner_grp + len('<control type="group">'):]

                c_idx = blk.find("<!-- C (Carlos")
                if c_idx != -1:
                    popup_grp_start = blk.rfind('<control type="group">', 0, c_idx)
                    if popup_grp_start != -1:
                        popup_blk = blk[popup_grp_start:]
                        popup_blk = re.sub(
                            r'<left>-15</left>\s*<top>-6</top>\s*<width>500</width>\s*<height>288</height>\s*<texture colordiffuse="\$VAR\[FlixAccentW\]">flix/frame_500x288\.png</texture>',
                            '<left>-14</left>\n\t\t\t\t\t\t\t\t<top>-6</top>\n\t\t\t\t\t\t\t\t<width>620</width>\n\t\t\t\t\t\t\t\t<height>354</height>\n\t\t\t\t\t\t\t\t<texture border="24" colordiffuse="$VAR[FlixAccentW]">flix/focus_border.png</texture>',
                            popup_blk,
                            count=1
                        )
                        popup_blk = re.sub(r'<left>-7</left>\s*<top>2</top>\s*<width>484</width>\s*<height>272</height>', '<left>-8</left>\n\t\t\t\t\t\t\t\t<top>0</top>\n\t\t\t\t\t\t\t\t<width>608</width>\n\t\t\t\t\t\t\t\t<height>342</height>', popup_blk, count=1)
                        popup_blk = re.sub(r'<left>-7</left>\s*<top>124</top>\s*<width>484</width>\s*<height>150</height>', '<left>-8</left>\n\t\t\t\t\t\t\t\t<top>188</top>\n\t\t\t\t\t\t\t\t<width>608</width>\n\t\t\t\t\t\t\t\t<height>170</height>', popup_blk, count=1)
                        popup_blk = re.sub(r'<top>166</top>\s*<width>235</width>\s*<height>94</height>', '<top>232</top>\n\t\t\t\t\t\t\t\t<width>275</width>\n\t\t\t\t\t\t\t\t<height>110</height>', popup_blk, count=1)
                        blk = blk[:popup_grp_start] + popup_blk

                return blk

            content = replace_include_block(content, "FlixRowLayouts", patch_row_layouts)

            def patch_card_overlay(blk):
                blk = blk.replace('<param name="px">12</param>', '<param name="px">18</param>')
                blk = blk.replace('<top>12</top>', '<top>10</top>')
                blk = re.sub(r'<width>168</width>(\s*)<height>252</height>', r'<width>244</width>\1<height>366</height>', blk)
                blk = re.sub(r'<width>148</width>(\s*)<height>252</height>', r'<width>224</width>\1<height>366</height>', blk)
                blk = re.sub(r'<top>172</top>(\s*)<width>168</width>(\s*)<height>80</height>', r'<top>270</top>\1<width>244</width>\2<height>80</height>', blk)
                blk = re.sub(r'<top>176</top>(\s*)<width>152</width>(\s*)<height>72</height>', r'<top>274</top>\1<width>228</width>\2<height>72</height>', blk)
                return blk

            content = replace_include_block(content, "FlixCardOverlay", patch_card_overlay)

            def patch_more_page(blk):
                lines = [
                    '<control type="list" id="7301">',
                    '\t\t\t\t\t<left>128</left>',
                    '\t\t\t\t\t<top>400</top>',
                    '\t\t\t\t\t<width>1792</width>',
                    '\t\t\t\t\t<height>336</height>',
                    '\t\t\t\t\t<onup condition="Integer.IsGreater(Container(7300).NumItems,0)">7300</onup>',
                    '\t\t\t\t\t<onup condition="!Integer.IsGreater(Container(7300).NumItems,0) + $PARAM[upc]">$PARAM[up]</onup>',
                    '\t\t\t\t\t<onup condition="!Integer.IsGreater(Container(7300).NumItems,0) + $PARAM[up2c]">$PARAM[up2]</onup>',
                    '\t\t\t\t\t<!-- sin vuelta al principio/final --><ondown>noop</ondown><onleft>noop</onleft><onright>noop</onright>',
                    '\t\t\t\t\t<orientation>horizontal</orientation>',
                    '\t\t\t\t\t<focusposition>0</focusposition>',
                    '\t\t\t\t\t<movement>0</movement>',
                    '\t\t\t\t\t<scrolltime tween="sine" easing="out">350</scrolltime>',
                    '\t\t\t\t\t<preloaditems>2</preloaditems>',
                    '\t\t\t\t\t<itemlayout width="232" height="328">',
                    '\t\t\t\t\t\t<control type="image">',
                    '\t\t\t\t\t\t\t<left>16</left>',
                    '\t\t\t\t\t\t\t<top>12</top>',
                    '\t\t\t\t\t\t\t<width>200</width>',
                    '\t\t\t\t\t\t\t<height>300</height>',
                    '\t\t\t\t\t\t\t<aspectratio scalediffuse="false">scale</aspectratio>',
                    '\t\t\t\t\t\t\t<texture background="true" colordiffuse="FFBFBFBF" diffuse="Palantir/masks/poster.png" fallback="DefaultVideo.png">$INFO[ListItem.Art(poster)]</texture>',
                    '\t\t\t\t\t\t</control>',
                    '\t\t\t\t\t</itemlayout>',
                    '\t\t\t\t\t<focusedlayout width="232" height="328">',
                    '\t\t\t\t\t\t<control type="group">',
                    '\t\t\t\t\t\t\t<animation effect="zoom" start="100" end="105" center="auto" time="150" tween="sine" condition="Control.HasFocus(7301)">Conditional</animation>',
                    '\t\t\t\t\t\t\t<control type="image">',
                    '\t\t\t\t\t\t\t\t<left>16</left>',
                    '\t\t\t\t\t\t\t\t<top>12</top>',
                    '\t\t\t\t\t\t\t\t<width>200</width>',
                    '\t\t\t\t\t\t\t\t<height>300</height>',
                    '\t\t\t\t\t\t\t\t<aspectratio scalediffuse="false">scale</aspectratio>',
                    '\t\t\t\t\t\t\t\t<texture background="true" colordiffuse="FFBFBFBF" diffuse="Palantir/masks/poster.png" fallback="DefaultVideo.png">$INFO[ListItem.Art(poster)]</texture>',
                    '\t\t\t\t\t\t\t</control>',
                    '\t\t\t\t\t\t\t<control type="image">',
                    '\t\t\t\t\t\t\t\t<left>10</left>',
                    '\t\t\t\t\t\t\t\t<top>6</top>',
                    '\t\t\t\t\t\t\t\t<width>226</width>',
                    '\t\t\t\t\t\t\t\t<height>312</height>',
                    '\t\t\t\t\t\t\t\t<texture border="24" colordiffuse="$VAR[FlixAccentW]">flix/focus_border.png</texture>',
                    '\t\t\t\t\t\t\t\t<visible>Control.HasFocus(7301)</visible>',
                    '\t\t\t\t\t\t\t</control>',
                    '\t\t\t\t\t\t</control>',
                    '\t\t\t\t\t</focusedlayout>',
                    '\t\t\t\t</control>',
                ]
                new_list_7301 = newline.join(lines)

                start_m = re.search(r'<control\s+type="list"\s+id="7301"\s*>', blk)
                if not start_m:
                    return blk
                s_pos = start_m.start()
                token_re = re.compile(r'(<control\b[^>]*>|</control>)', re.IGNORECASE)
                depth = 0
                e_pos = -1
                for m in token_re.finditer(blk, s_pos):
                    if not m.group(1).lower().startswith("</control"):
                        depth += 1
                    else:
                        depth -= 1
                        if depth == 0:
                            e_pos = m.end()
                            break
                if e_pos == -1:
                    return blk
                return blk[:s_pos] + new_list_7301 + blk[e_pos:]

            content = replace_include_block(content, "FlixMorePage", patch_more_page)

            def patch_eps_cards(blk):
                return blk.replace('<param name="zoom" value="115" />', '<param name="zoom" value="104" />')

            content = replace_include_block(content, "FlixEpsCards", patch_eps_cards)

            def revert_hero_plot(blk):
                blk = re.sub(
                    r'<control type="textbox">\s*<left>0</left>\s*<top>318</top>\s*<width>880</width>\s*<height>155</height>(\s*<font>font23_narrow</font>\s*<textcolor>FFCCCCCC</textcolor>\s*)<label>\$INFO\[ListItem\.Plot\]</label>',
                    r'<control type="textbox">\n\t\t\t\t\t<left>0</left>\n\t\t\t\t\t<top>318</top>\n\t\t\t\t\t<width>820</width>\n\t\t\t\t\t<height>60</height>\1<label>$VAR[FlixPlot2]</label>',
                    blk,
                    count=1
                )
                return blk

            content = replace_include_block(content, "FlixHero", revert_hero_plot)

            def revert_hero_frozen_plot(blk):
                blk = re.sub(
                    r'<control type="textbox">\s*<left>0</left>\s*<top>\$PARAM\[plot\]</top>\s*<width>880</width>\s*<height>155</height>',
                    r'<control type="textbox">\n\t\t\t\t\t<left>0</left>\n\t\t\t\t\t<top>$PARAM[plot]</top>\n\t\t\t\t\t<width>820</width>\n\t\t\t\t\t<height>60</height>',
                    blk,
                    count=1
                )
                return blk

            content = replace_include_block(content, "FlixHeroFrozen", revert_hero_frozen_plot)

            if content != original:
                content = re.sub(r'(<includes\b[^>]*>)', r'\1' + newline + MARKER, content, count=1)
                with open(XML_PATH, "w", encoding="utf-8") as f:
                    f.write(content)
                log("Includes_Flix.xml parcheado (V21)")
                changed = True

    if os.path.exists(INICIO_XML_PATH):
        with open(INICIO_XML_PATH, "r", encoding="utf-8") as f:
            inicio_txt = f.read()

        if INICIO_MARKER not in inicio_txt:
            for old_im in (
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V20_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V19_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V18_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V17_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V16_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V15_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V14_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V13_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V12_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V11_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_V10_OK -->",
                "<!-- PATCH_YOSEBA_INICIO_TOP10_OK -->",
            ):
                inicio_txt = inicio_txt.replace(old_im + "\r\n", "").replace(old_im + "\n", "").replace(old_im, "")

            newline_i = "\r\n" if "\r\n" in inicio_txt else "\n"
            orig_i = inicio_txt

            inicio_txt = re.sub(
                r'(<param name="top10" value="true" />\s*)<param name="itemw" value="(?:236|274|310)" />(\s*<param name="px" value="56" />)',
                r'\1<param name="itemw" value="330" />\2',
                inicio_txt
            )

            if inicio_txt != orig_i:
                inicio_txt = re.sub(r'(<window\b[^>]*>)', r'\1' + newline_i + INICIO_MARKER, inicio_txt, count=1)
                with open(INICIO_XML_PATH, "w", encoding="utf-8") as f:
                    f.write(inicio_txt)
                log("FlixInicio.xml parcheado: separación Top 10 (itemw=330)")
                changed = True

    return changed


if __name__ == "__main__":
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        if patch_flix_xml():
            xbmc.executebuiltin("ReloadSkin()")
        if monitor.waitForAbort(15):
            break
