import tkauto

if __name__ == '__main__':
    ui = tkauto.UI()
    ui.create_tabview(raiz=ui.root,
                      name="tabview1",
                      x=0,
                      y=0,
                      width=1,
                      height=1,
                      isRelativePos=True,
                      isRelativeScl=True,
                      tabListNames=["tab1", "tab2", "tab3", "tab4"]
                      )

    xpos = 0.01
    contraancho = 1 - (xpos * 2)
    ui.create_scrollableframe(raiz=ui.element_searcher("tabview_list", "tabview1").data.tab("tab1"),
                              name="sframe1",
                              x=0, y=0,
                              width=1, height=0.7,
                              isRelativePos=True, isRelativeScl=True
                              )

    ui.create_label(raiz=ui.element_searcher("scrollableframe_list", "sframe1").data,
                    name="label1",
                    x=0,
                    y=0,
                    width=1,
                    height=1,
                    isRelativePos=True,
                    isRelativeScl=True,
                    text="",
                    text_color="#FFFFFF",
                    font=""
                    )

    ui.create_textbox(raiz=ui.element_searcher("tabview_list", "tabview1").data.tab("tab1"),
                      name="box2",
                      x=xpos,
                      y=0.72,
                      width=contraancho,
                      height=0.2,
                      isRelativePos=True,
                      isRelativeScl=True,
                      isReadOnly=False
                      )
    ui.run()
