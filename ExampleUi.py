#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 19:52:58 2020

@author: pi
"""

def _unittest_task_statistics_widget():
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication([])
    win = QMainWindow()
    win.resize(800, 600)

    async def update_delegate() -> TaskStatisticsView:
        print('UPDATE')
        return _make_test_data()

    widget = TaskStatisticsWidget(win, update_delegate)

    win.setCentralWidget(widget)
    win.show()

    async def run_events():
        for _ in range(1000):
            app.processEvents()
            await asyncio.sleep(0.005)

        win.close()

    asyncio.get_event_loop().run_until_complete(run_events())