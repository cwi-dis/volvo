To prepare new artwork by Evan (saved as SVG with bitmaps inlined) do the following steps:
- Remove the preamble, everything before the <svg> tag (about 10 lines).
- Insert the content of svg-defs somewhere near the top (inside the first <g> element for example)
- Set the fill pattern of the hand segments correctly by adding
  	style="fill: url(#handfill)"
  to the polygons in group _x3C_hand_x5F_fill_x5F_group_x3E_ (which is
  inside group Hand_x5F_Action)
- Compare the result to ../production/server/public/img/volvo_graphic.svg to double
  check I haven't forgotten anything, there may be a few other IDs that need changing.
- Finally copy the new artwork to ../production/server/public/img/volvo_graphic.svg
