#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ипморт библиотеки для работы с интерпретатором
import sys

# несколько строк для решения проблем с кодировкой русского текста
reload(sys)
sys.setdefaultencoding('utf-8')

"""
Программа расчета электрического обогрева нефтяных скважин.
"""  
#------------------------------------------------------------------------------

# Импортируемые библиотеки

# Библиотека для работы с wxWidgets
import wx

# Библиотека для работы с Ribbon
import wx.lib.agw.ribbon as RB

# Библиотека для использования html текста
import wx.html as html

# Библиотека для работы с файловой системой (открытие и сохранение файлов через диалоговые окна)
import os

# Библиотеки для работы с продвинутым ноутбуком
import wx.lib.agw.aui as aui

import wx.aui

# Библиотека для работы со временем и датами
from time import strftime

#import logging

import wx.lib.plot as plot

# Библиотека используется для 
import wx.adv


# from __future__ import print_function

# Библиотеки для работы с графикой
import matplotlib 

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
  
from matplotlib.figure import Figure

# Библиотека для работы с матрицами, загрузка данных из файла
import numpy

import numpy as np

from numpy import loadtxt

# библиотека для работы с датами и временем
import time

# библиотека для построения графиков
import matplotlib.pyplot as plt

# библиотека для разметки осей графика
from matplotlib.ticker import MultipleLocator

# Библиотека для работы с таблицей
import wx.grid as  gridlib

# import threading

# from PIL import Image

#start
# start = time.clock()

# start = time.time()
#----------------------------------------------------------------------
# Идентификаторы для кнопок меню в функциональном окне

ID_OpenFile = wx.NewIdRef()        # открытие файла
ID_SaveAsFile = wx.NewIdRef()      # сохранение файла (если необходимо)
ID_SetData = wx.NewIdRef()         # ввод анкетных данных
ID_ImportData = wx.NewIdRef()      # импорт данных (считывание и обработка данных перед расчетом)
ID_Run  = wx.NewIdRef()            # запуск расчета
ID_Plot = wx.NewIdRef()            # рисуем график
ID_CreateReport = wx.NewIdRef()    # создаем отчет
ID_ViewReport = wx.NewIdRef()      # просмотр отчета
ID_PrintReport = wx.NewIdRef()     # печать отчета
ID_Help = wx.NewIdRef()            # помощь


####################################################################################

class MainFrame(wx.Frame):
    """ 
    Создаем основное окно программы из которого будет вызываться 
    функциональное окно, используя которое можно получить результат расчета    """
#------------------------------------------------------------------------------
# Создаем фрейм
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        
        self.InitUI()
    
# Создаем меню
#------------------------------------------------------------------------------
    def InitUI(self):

        # Создаем панель меню
        menubar = wx.MenuBar()
        
        # Создаем меню 
        fileMenu = wx.Menu()
        
        # Создаем пункт меню 'Выход' с комбинацией быстрых клавиш
        quitItem = fileMenu.Append(wx.ID_EXIT, u'&Выход\tCtrl+Q', 'нажмите для выхода из программы')
    
        # Создаем меню 'Файл'
        menubar.Append(fileMenu, u'Файл')
        
        # Показываем панель меню
        self.SetMenuBar(menubar)
      
        #Создаем пункт меню 'Справка'
        helpMenu = wx.Menu()
    
        # Создаем пунк меню О программе
        aboutItem = helpMenu.Append(wx.ID_ABOUT, u"О программе", ' сведения о программе')

        # Создаем меню Справка
        menubar.Append(helpMenu, u'Справка')
        
        self.SetMenuBar(menubar)
        
#***************************************************************************************    
     
        """ При необходимости, здесь пишем код для дополнительных пунктов меню """ 
        
#****************************************************************************************

#---------------- Обрабатываем события из меню --------------------------------------------

        # Выходим из главного окна программы при нажатии 'Выход' 
        self.Bind(wx.EVT_MENU, self.OnQuit, quitItem)
        
        # Вызываем окно справки 'О программе'
        self.Bind(wx.EVT_MENU, self.AboutMessage, aboutItem)
        
#-------------------------------------------------------------------------------------------        
# Задаем дополнительные параметры основного окна
       
    # Задаем размер подменю 
        self.SetSize((300, 250))
        
        # Устанавливаем цвет фона
        self.SetBackgroundColour('#87857C')
        
        # Расположение
        self.Centre()

        # Создаем строку состояния StatusBar
        self.CreateStatusBar()
        
        # Выводим в нем приветствие
        self.PushStatusText("Добро пожаловать в программу")

#----------------- Создаем иконки ToolBar -----------------------------------------------------
    
        # Создаем панель
        toolbar = self.CreateToolBar()
        
        # Добавляем картинку значка
        ToolBarFirstIcon = toolbar.AddTool(wx.ID_ANY, 'Data', wx.Bitmap('Picture\ESP1.jpg'), shortHelp="расчет обогрева скважины с ЭЦН")
        
        # Добавляем дополнительные иконки
        ToolBarSecondIcon = toolbar.AddTool(wx.ID_ANY, 'Data', wx.Bitmap('Picture\Oil pump.jpg'), 
                                      shortHelp="расчет обогрева скважины со станком-качалкой")
        
        ToolBarThirdIcon = toolbar.AddTool(wx.ID_ANY, 'Data', wx.Bitmap('Picture\Lift.jpg'), shortHelp="расчет обогрева скважины газлифт")
        
        ToolBarFifthIcon = toolbar.AddTool(wx.ID_ANY, 'Data', wx.Bitmap('Picture\Pump.jpg'), 
                                           shortHelp="расчет обогрева скважины с винтовым насосом")
        
        
        # Делаем пенель видимой
        toolbar.Realize()

#------------ Вызываем функциональное окно программы -------------------------------------------

        # Кликаем мышкой по иконке и вызываем функциональное окно программы OnRibbonBar
        self.Bind(wx.EVT_TOOL, self.OnRibbonBar, ToolBarFirstIcon)
        
#-------- Задаем параметры главного окна --------------------------------------------------
        
        # Задаем размеры главного окна
        self.SetSize((400, 300))
        
        # Указываем название главного окна
        self.SetTitle(u'Обогрев скважины')
        
        # Задаем расположение
        self.Centre()

#----------------- Добавляем иконку в верхний левый угол главного окна ---------------------------

        self.panel = wx.Panel(self, wx.ID_ANY)
        
        # Размещаем картинку
        icon = wx.Icon('Picture\o&g1.jpg', wx.BITMAP_TYPE_JPEG)
        
        # Показываем в окне
        self.SetIcon(icon)
        
#***************************************************************************************************  
#                Процедуры
#**************************************************************************************************

    def OnQuit(self, event):
        """ Закрываем главное окно  """
        self.Close()
#--------------------------------------------------------------------------------------------------------  
#
    def AboutMessage(self, event):
        
        """ Выдодим окно справки """
        
        # Выводим информационное сообщение
        info = wx.adv.AboutDialogInfo()
        
        # Создаем шаблон для описания
        desc = ["\n Программа позволяет проводится теплотехнический расчет работы нефтяной скважины по данным технологической анкеты.\n",
                "Вводятся начальные данные по скважине. Строится геотерма скважины. Определяются теплопотери в грунт.",
                "Строится термограмма скважины с учетом характера движения жидкости. Определяется глубина отложения парафинов и проводится расчет параметров электрического кабеля.\n",
                "Информация о платформе: (%s,%s)\n",
                "Лицензия: частная"]
        desc = "\n".join(desc)
        
        # Получаем информацию по системе
        py_version = [sys.platform, ", python ", sys.version.split()[0]]
        platform = list(wx.PlatformInfo[1:])
        platform[0] += (" " + wx.VERSION_STRING)
        wx_info = ", ".join(platform)

        # Заполняем поля 
        info.SetName("Программа расчета обогрева нефтяных скважин\n")
        info.SetVersion("Версия 1.0")
        info.SetCopyright("Copyright (C) ОКБ <<Гамма>>")
        info.SetDescription(desc % (py_version, wx_info))
        info.SetWebSite("https://okb-gamma.ru/")
        info.AddDeveloper("Инженер-разработчик исследовательской группы ОГК, Гераськин Игорь Сергеевич")

        # Создаем и показываем диалог
        wx.adv.AboutBox(info)

#--------------------------------------------------------------------------------------------------------
# 
    def OnRibbonBar(self, event):
        """ Вызываем функциональное окно по нажатию на значок    """
        
        # Создаем диалоговое окно
        dlg = RibbonBar(None, title="Скважина с ЭЦН - Новый расчет", size=(420, 180))
        
        # Показываем его
        dlg.ShowModal()
        
#----------------------------------------------------------------------------------------------------------
# Запускаем главное окно программы
def main():
    
    app = wx.App()
    ex = MainFrame(None)
    ex.Center()
    ex.Show()
    
    app.MainLoop()
    

#######################################################################################################################
class RibbonBar(wx.Dialog):
    """
    Создаем функциональное окно программы
    
    """
#---------------------------------------------------------------------------------------------------------------------
    def __init__(self, *ls, **kw):
        wx.Dialog.__init__(self, *ls, **kw)
        
        global setCalcPanel, ImportDataPanel, setResult, setDataPanel
        
#****************************** Создаем вкладку Главная **********************************************************

        """ В данной вкладке находятся стандартные 
              инструменты для работы с данными - значки Открыть и Сохранить как """
    
        # Создаем панель закладок        
        ribbonBar = RB.RibbonBar(self, wx.ID_ANY, agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE|RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)
        
        # Создаем вкладку Главная
        HomepageTab = RB.RibbonPage(ribbonBar, wx.ID_ANY, "Главная")
        
        # Создаем панель Стандартные
        HomepagePanel = RB.RibbonPanel(HomepageTab, wx.ID_ANY, u"Стандартные")
        
        # Размещаем панель на вкладке    
        setHomepagePanel = RB.RibbonButtonBar(HomepagePanel)
        
#------------------------------ Рисуем значки -----------------------------------------------------------         
        # Открыть
        HomepageIconOpen = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(48, 48))
   
        # Определяем значок 'Сохранить как' кнопки (выбираем из ряда стандартных)
        HomepageIconSaveAs = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_OTHER, wx.Size(48, 48))
       
        # Задаем название значка и рисуем его
        setHomepagePanel.AddSimpleButton(ID_OpenFile, u"Открыть", HomepageIconOpen, 'открыть файл')
        
        # Вызываем окно 'Открыть'
        setHomepagePanel.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnOpenFileRibbon, id=ID_OpenFile)
        
        # Задаем название значка и рисуем его
        setHomepagePanel.AddSimpleButton(ID_SaveAsFile, u"Сохранить как", HomepageIconSaveAs, 'сохранить файл с указанием имени')
        
         # Вызываем окно 'Открыть'
        setHomepagePanel.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSaveAsFileRibbon, id=ID_SaveAsFile)
        
#******************************** Создаем вкладку Инструменты ***********************************************

        """ В данной вкладке находятся следующие инструменты:
            - Ввод данных
            - Пуск
            А на одной панели:
            - Создать отчет
            - Просмотр отчета
            - Построить график
            - Печать отчета
            
         """
      
        # Создаем вкладку Инструменты
        ToolsTab = RB.RibbonPage(ribbonBar, wx.ID_ANY, "Инструменты")
        
        # Делаем вкладку Инструменты активной 
        ribbonBar.SetActivePage(ToolsTab)
        
        # Создаем панель 'Данные'
        DataPanel = RB.RibbonPanel(ToolsTab, wx.ID_ANY, "Данные")
        
        # Размещаем панель на вкладке
        setDataPanel = RB.RibbonButtonBar(DataPanel)
           
        # Задаем рисунок значка
        ToolsIconSetData = wx.Bitmap("Picture\Menu icons\data1.jpg", wx.BITMAP_TYPE_ANY)
        
        # Задаем название значка и всплывающей подсказки
        setDataPanel.AddSimpleButton(ID_SetData, "Ввод данных", ToolsIconSetData, 'ввести данные для расчета')
        
        # Вызываем окно 'Ввод данных'
        setDataPanel.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnOpenNewWindow, id=ID_SetData)
        
#------------------------ Создаем панель Импорт данных --------------------------------------------------------------

#         # Создаем панель 'Импорт данных'
#         DataImportPanel = RB.RibbonPanel(ToolsTab, wx.ID_ANY, "Подготовка данных")
        
#         # Размещаем панель на вкладке
#         ImportDataPanel = RB.RibbonButtonBar(DataImportPanel)
        
#         # Задаем рисунок значка
#         ToolsIconImportData = wx.Bitmap("import2.jpg", wx.BITMAP_TYPE_JPEG)
        
#         # Задаем название значка и всплывающей подсказки
#         ImportDataPanel.AddSimpleButton(ID_ImportData, "Подготовка данных", ToolsIconImportData, 'подготовить данные для расчета')
        
#         # Вызываем окно 'Ввод данных'
#         ImportDataPanel.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnImportData, id=ID_ImportData)
        
            
#----------------------- Создаем панель Расчет ------------------------------------------------------------------------

        CalcPanel = RB.RibbonPanel(ToolsTab, wx.ID_ANY, "Расчет")
     
        # Размещаем панель на вкладке
        setCalcPanel = RB.RibbonButtonBar(CalcPanel)
        
        # Задаем рисунок значка
        ToolsIconRunButton = wx.Bitmap( "Picture\Menu icons\Run1.jpg", wx.BITMAP_TYPE_ANY)
        
#-------------------------- Создаем панель Пуск ---------------------------------------------------------------------
        
        # Задаем название кнопки и значок
        setCalcPanel.AddSimpleButton(ID_Run, "Пуск", ToolsIconRunButton, 'запустить расчет')
        
        # Вызываем окно 'Пуск'
        setCalcPanel.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnRunCalculation, id=ID_Run)
        
#------------------------ Создаем панель Результаты расчета -------------------------------------------------------

        PlotPanel = RB.RibbonPanel(ToolsTab, wx.ID_ANY, "Обработка результатов")
        
        # Размещаем панель на вкладке
        setResult = RB.RibbonButtonBar(PlotPanel)
        
        # Задаем рисунок значка
        TooslIconPlot = wx.Bitmap( "Picture\Menu icons\plot.jpg", wx.BITMAP_TYPE_ANY)
        
#------------------------ Создаем кнопку Создать отчет -----------------------------------------------------------------

        # Задаем рисунок значка
        ToolsIconReport = wx.Bitmap( "Picture\Menu icons\Report.jpg", wx.BITMAP_TYPE_ANY )
    
        # Создаем кнопку Создать отчет
        setResult.AddSimpleButton(ID_CreateReport, "Создать отчет", ToolsIconReport, 'создать отчет')
      
         # Вызываем окно 'Создать отчет'
        setResult.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnCreateReport, id=ID_CreateReport)
        
#----------------------------- Создаем кнопку Просмотр отчета ---------------------------------------------------------- 
        # Задаем рисунок значка
        ToolsIconReview = wx.Bitmap( "Picture\Menu icons\open.jpg", wx.BITMAP_TYPE_ANY )
       
        # Создаем кнопку Просмотр отчета
        setResult.AddSimpleButton(ID_ViewReport, "Просмотр отчета", ToolsIconReview, 'открыть отчет для просмотра')
      
        # Вызываем окно 'Просмотр отчета'
        setResult.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnOpenViewer, id=ID_ViewReport)  
        
#----------------------------- Создаем кнопку Построить график -------------------------------------------------------------        
        
    # Создаем кнопку Построить график
        setResult.AddSimpleButton(ID_Plot, "График", TooslIconPlot, 'построить график')
        
        # Вызываем окно 'Построить график'        
        setResult.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnPlotGraph, id=ID_Plot)

#----------------------------- Создаем кнопку Печать отчета -------------------------------------------------------------
        # Задаем рисунок значка
        ToolsIconPrint = wx.Bitmap( "Picture\Menu icons\print2.jpg", wx.BITMAP_TYPE_ANY )
        
        # Создаем кнопку Печать отчета
        setResult.AddSimpleButton(ID_PrintReport, "Печать отчета", ToolsIconPrint, 'напечатать отчет')       
        
        # Вызываем окно 'Просмотр отчета'
        setResult.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onPrintDocument, id=ID_PrintReport)
        
#**************************************** Создаем вкладку Справка **************************************************************
    
        #Создаем вкладку Справка
        infoTab = RB.RibbonPage(ribbonBar, wx.ID_ANY, "Справка")
    
        # Создаем панель Информация
        HelpPanel = RB.RibbonPanel(infoTab, wx.ID_ANY, "Информация")
        
        # Размещаем панель на вкладке
        helpinfo = RB.RibbonButtonBar(HelpPanel)

        # Задаем рисунок значка
        HelpIcon = wx.Bitmap( "Picture\Menu icons\help.jpg", wx.BITMAP_TYPE_ANY)
        
        # Создаем кнопку и ее название
        helpinfo.AddSimpleButton(ID_Help, "Помощь", HelpIcon, 'справочные метериалы по программе')
    
        # Вызываем меню 'Помощь'
        helpinfo.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onOpenHelpWindow, id=ID_Help)
        
        # Показываем панель 
        ribbonBar.Realize()
        
        # Выравниваем        
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(ribbonBar, 0, wx.EXPAND)
        self.SetSizer(s)
        
#---------------------------------------------------------------------------------------------------------------------        
 # Управляем видимостью иконок на функциональной панели
    
 # Начальная установка кнопок - активны только 'Ввод данных' и 'Помощь'
    
        # Активность кнопки 'Открыть'  
        setHomepagePanel.EnableButton(ID_OpenFile, True)
        
        # Активность кнопки 'Сохранить как'  
        setHomepagePanel.EnableButton(ID_SaveAsFile, False)
        
        # Активность кнопки 'Ввод данных'  
        setDataPanel.EnableButton(ID_SetData, True)
        
#         # Активность кнопки 'Импорт данных'  
#         ImportDataPanel.EnableButton(ID_ImportData, False)
        
        # Активность кнопки 'Пуск'  
        setCalcPanel.EnableButton(ID_Run, False)
        
        # Активность кнопки 'Создать отчет' 
        setResult.EnableButton(ID_CreateReport, False)
        
        # Активность кнопки 'Просмотр отчета' 
        setResult.EnableButton(ID_ViewReport, False)
        
        # Активность кнопки 'Построить график'  
        setResult.EnableButton(ID_Plot, False)
        
        # Активность кнопки 'Печать отчета' 
        setResult.EnableButton(ID_PrintReport, False)
        
        # Активность кнопки 'Помощь' 
        helpinfo.EnableButton(ID_Help, True)

#*********************************************************************************************************
# Открываем файл для просмотра
   
    def OnOpenFileRibbon(self, event):
        
        wildcard = "Text file (*.txt)|*.txt|"     \
                   "Python source (*.py)|*.py|"     \
                   "MS Office documents (*.doc)|*.doc|" \
            "All files (*.*)|*.*"     
  
        # Создаем окно
        frame = wx.Frame(None, title="Открываем файл", size=(800, 700))
        
        # Создаем окно многострочного текста и открываем его во фрейме
        self.my_text = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
        
        self.my_text.SetFont(wx.Font(FONTSIZE, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))
       
        # Выбираем текущую рабочую директорию
        self.currentDirectory = os.getcwd()
        
        # Открываем диалог и выбираем файл        
        dialog = wx.FileDialog(None, message="Открытие документа", defaultDir= self.currentDirectory, 
                            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dialog.ShowModal() == wx.ID_OK:
            # This returns the file that was selected
            path = dialog.GetPath()

        # Открываем файл только для чтения
            fileopen = open(path, 'r')
            self.my_text.SetValue(fileopen.read())
            fileopen.close()  
    
        # Показываем окно
        frame.Show()
        
#---------------------------------------------------------------------------------------------

  # сюда можно добавить, при необходимости, дополнительные пункты меню (пункты сохранить, сохранить как и выход)
    

#-------------------------------------------------------------------------------------------------------------
# Сохраняем файл как 

    def OnSaveAsFileRibbon(self, event):

        """
        Создаем и показываем диалоговое окно Сохранения файла
        
        """
        wildcard = "Text source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
        
        self.currentDirectory = os.getcwd()
        
        dlg = wx.FileDialog(self, message="Сохранение документа", defaultDir=self.currentDirectory, 
                            defaultFile="", wildcard=wildcard, style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            report = open(path, "w") 

            report.close()

        dlg.Destroy()

#---------------------------------------------------------------------------------------------------------------        

# Открываем окно Ввода данных

    def OnOpenNewWindow(self, event):
        
        """ открываем окно ввода данных """
        
        NewWindow = NotebookFrame(None)
        NewWindow.Show()
        
##################################################################################################  
#------------------------------------- Запускаем расчет -----------------------------------------#
##################################################################################################

#**********************************************************************************************************
#     def OnRunCalculation(self, evt):
        
#         """ запускаем расчет """      
        
        
# #         dialog = MyProgressDialog()
# #         dialog.Show()
# #         dialog.Destroy()

#         self.maxPercent = 100
#         self.percent = 0

#         self.StartThread(self.DoWork)

# #---------------------------------------------------------------------------------
#     def StartThread(self, func, *args):
        
#         """ обработка многопоточности """
        
#         thread = threading.Thread(target=func, args=args)
#         thread.setDaemon(True)
#         thread.start()

# #---------------------------------------------------------------------------------
#     def showProgress(self):
        
#         """ показываем окно прогресса """
        
#         self.progress = wx.ProgressDialog("Расчет выполняется", "пожалуйста, ждите ...", maximum=self.maxPercent, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)
        
# #         style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE
# #         style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE

# #-----------------------------------------------------------------------------------------------------------------------------
#     def destoryProgress(self):
        
#         """ удаляем окно прогресса """
        
#         self.progress.Destroy()

# #-----------------------------------------------------------------------------------------------------------------------------
#     def updateProgress(self, percent):
        
#         """ обновляем окно прогресса """
        
#         keepGoing = True
#         time.sleep(1)
#         while keepGoing and self.percent < percent:
#             self.percent += 1
#             (keepGoing, skip) = self.progress.Update(self.percent)
#             time.sleep(0.1)

# #-----------------------------------------------------------------------------------------------------------------------------
#     def doSomething(self, take_time, taskPercent, say_something):
        
#         """  """
        
#         time.sleep(take_time)
#         (keepGoing, skip) = self.progress.Update(taskPercent, say_something + " выполнено!")

# #-----------------------------------------------------------------------------------------------------------------------------
#     def DoWork(self):
        
#         """ выполняем зачачу """
        
#         self.StartThread(self.showProgress)

#         taskPercent = 25
#         self.StartThread(self.updateProgress, taskPercent)
#         self.doSomething(5, taskPercent, "1st")

#         taskPercent +=25
#         self.StartThread(self.updateProgress, taskPercent)
#         self.doSomething(5, taskPercent, "2nd")

#         taskPercent +=25
#         self.StartThread(self.updateProgress, taskPercent)
#         self.doSomething(5, taskPercent, "3rd")

#         taskPercent +=25
#         self.StartThread(self.updateProgress, taskPercent)
#         self.doSomething(5, taskPercent, "4th")
        
        

#         self.destoryProgress()

#         # Показываем сообщение что расчет выполнен успешно 
#         wx.MessageBox('Расчет выполнен успешно!', 'Сообщение', wx.OK | wx.ICON_INFORMATION)

        
#     #  После расчета выключаем кнопки

#           # Активность кнопки 'Пуск'  
#         setCalcPanel.EnableButton(ID_Run, False)
        
#     # Включаем поля по окончанию расчета
       
#         # Активность кнопки 'Создать отчет' 
#         setResult.EnableButton(ID_CreateReport, True)
#************************************************************************************************************************
    def OnRunCalculation(self, evt):
        
        """ запускаем расчет """  
        
        dialog = MyProgressDialog()
        dialog.Show()
        
        # Показываем сообщение что расчет выполнен успешно 
        wx.MessageBox('Расчет выполнен успешно!', 'Сообщение', wx.OK | wx.ICON_INFORMATION) 
        
        dialog.Destroy() 
        #  После расчета выключаем кнопки

        # Активность кнопки 'Пуск'  
        setCalcPanel.EnableButton(ID_Run, False)
        
        # Включаем поля по окончанию расчета
       
        # Активность кнопки 'Создать отчет' 
        setResult.EnableButton(ID_CreateReport, True)
        
########################################################  
#-------------- 'Создаем отчет' -----------------------#
########################################################

    def OnCreateReport(self, event):
        
        """ создаем отчет """
  
        wildcard = "Text source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
        self.currentDirectory = os.getcwd()
        dlg = wx.FileDialog(self, message="Создание отчета", defaultDir=self.currentDirectory, 
                            defaultFile="", wildcard=wildcard, style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            report = open(path, "w") 

    # Создаем заголовочный файл

        # Устанавливаем дату и время
        date = strftime("%a %d-%m-%y %H:%M:%S")

        # Добавляем линию конеца заголовочного файла
        div = '************************************************************************'

        # Записываем заголовочные данные в файл 
        
        report.write('Наименование: Отчет')
        
        report.write('\n')
    
#         self.multiline = """\n Программа позволяет проводится теплотехнический расчет работы нефтяной скважины по данным технологической анкеты.
# \n Вводятся начальные данные по скважине. Строится геотерма скважины. Определяются теплопотери в грунт.
# \n Строится термограмма скважины с учетом характера движения жидкости. Определяется глубина отложения
# \n парафинов и проводится расчет параметров электрического кабеля.

# \n Выходными параметрами программы являются: \n
# - длины обогрева (горячая и холодная зона) \n
# - электротехнические параметры кабеля (мощность обогрева, ток, напряжение) \n
# - температура жилы и оболочки \n """
        
#         report.write('\n Описание: Программа расчета электрического обогрева нефтяных скважин с ЭЦН.\n %s' % self.multiline)

        report.write('\n Описание: Расчет электрического обогрева нефтяной скважин с ЭЦН.')
        
        report.write('\n')
        
        report.write('\n Разработчик: ООО ОКБ "Гамма"')
        
        report.write('\n')
        
        report.write('\n Дата расчета:' + date)
        
        report.write('\n')
        
        # считываем данные из файла
        with open (thispath, "r") as myfile:
            data=myfile.readlines()
            
        # удаляем лишние строчки
        del data[0:8]

        # преобразуем list в string
        newvalue = "".join(data)

        # разделяем строку
        splitedData = newvalue.split()

        # удаляем весь текст, оставляем только значение
        del splitedData[:5]

        # присваиваем значение переменной
        DownholeNumber = splitedData[0]
        
        # Записываем полученное значение в файл отчета
        report.write('\n Cкважина №: %s' % DownholeNumber)
        
        report.write('\n')
        
        # добавляем разделитель
        report.write('\n' + div * 1 + '\n')
        
#-------------------------------------------------------------------------------------------------------

        report.write('\n Температура парафинизации в устье скважины:')
        
        report.write('\n')
        
        report.write('\n Интервал регулирования температуры системой управления:' )
        
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
        
#-------------------------------------------------------------------------------------------------------
        report.write('\n Номинальный дебит скважины по жидкости:')
    
        report.write('\n')
    
        report.write('\n Минимальная глубина обогрева для номинального дебита:')
    
        report.write('\n')
        
        report.write('\n Длина нагревателя Stream Tracer 1.0/50 с запасом:')
    
        report.write('\n')
        
        report.write('\n В том числе: надземная часть')
    
        report.write('\n')
        
        report.write('\n Зона повышенной мощности (верхняя часть):')
    
        report.write('\n')
        
        report.write('\n Зона пониженной мощности (нижняя часть):')
    
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
        
#-------------------------------------------------------------------------------------------------------
        report.write('\n Напряжение питания для нагревателя длиной :')
    
        report.write('\n')
        
        report.write('\n Рабочий ток:')
    
        report.write('\n')
        
        report.write('\n Мощность нагревателя при номинальном дебите:')
    
        report.write('\n')
        
        report.write('\n Линейная мощность верхней зоны обогрева скважины:')
    
        report.write('\n')
        
        report.write('\n Линейная мощность нижней зоны обогрева скважины:')
    
        report.write('\n')
        
        report.write('\n Максимальная температура жилы при номинальном дебите:')
    
        report.write('\n')
        
        report.write ('\n Максимальная температура жилы (по алгоритму):')
        
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
    
#----------------------------------------------------------------------------------------------------------
        report.write('\n Минимальный дебит скважины по жидкости:')
    
        report.write('\n')
        
        report.write('\n Минимальная глубина обогрева для минимального дебита:')
    
        report.write('\n')
        
        report.write('\n Длина нагревателя Stream Tracer 1.0/50 с запасом:')
    
        report.write('\n')
        
        report.write('\n В том числе: надземная часть')
    
        report.write('\n')
        
        report.write('\n Зона повышенной мощнсти (верхняя часть):')
    
        report.write('\n')
        
        report.write('\n Зона пониженной мощности (нижняя часть):')
              
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
#---------------------------------------------------------------------------------------------------------------
        report.write('\n Напряжение питания для нагреывателя длиной :')
    
        report.write('\n')
        
        report.write('\n Рабочий ток:')
    
        report.write('\n')
        
        report.write('\n Мощность нагревателя при минимальном дебите:')
    
        report.write('\n')
        
        report.write('\n Линейная мощность верхней зоны обогрева скважины:')
    
        report.write('\n')
        
        report.write('\n Линейная мощность нижней зоны обогрева скважины:')
    
        report.write('\n')
        
        report.write('\n Максимальная температура жилы при минимальном дебите:')
    
        report.write('\n')
        
        report.write('\n Максимальная температура жилы (по алгоритму):')
    
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
#---------------------------------------------------------------------------------------------------------------
        report.write('\n Расчет для заданных: глубины обогрева')
    
        report.write('\n')
        
        report.write('\n и напряжения питания:')
    
        report.write('\n')
        
        report.write('\n Требуется нагреватель Stream Tracer 1.0/35 длиной:')
    
        report.write('\n')
        
        report.write('\n В том числе: надземная часть')
    
        report.write('\n')
        
        report.write('\n зона повышенной мощности (верхняя часть):')
    
        report.write('\n')
        
        report.write('\n зона пониженной мощности (нижняя часть):')
    
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
#-----------------------------------------------------------------------------------------------------------------
        
        report.write('\n При номинальном дебите:')
        
        report.write('\n')
        
        report.write('\n ожидаемое значение рабочего тока:')
        
        report.write('\n')
        
        report.write('\n Мощность нагревателя составит:')
        
        report.write('\n')
        
        report.write('\n Линейная мощность верхней зоны обогрева скважины:')
        
        report.write('\n')
        
        report.write('\n Линейная мощность нижней зоны обогрева скважины:')
        
        report.write('\n')
        
        report.write('\n Расчетная температура флюида в устье скважины:')
        
        report.write('\n')
        
        report.write('\n Максимальная температура жилы при номинальном дебете:')
        
        report.write('\n')
        
        report.write('\n Максимальная температура жилы (по алгоритму):')
        
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
        
        report.write('\n')
            
        report.write(' конец ')
#----------------------------------------------------------------------
        # Закрываем окно с данными
     
        dlg.Destroy()
    
        # Показываем сообщение что все Ок 
        wx.MessageBox(u'Отчет успешно создан!', u'Сообщение', wx.OK | wx.ICON_INFORMATION)
        
         # Активность кнопки 'Создать отчет' 
        setResult.EnableButton(ID_CreateReport, False)
        
         # Активность кнопки 'Построить график'  
        setResult.EnableButton(ID_Plot, True)
        
        # Активность кнопки 'Просмотр отчета' 
        setResult.EnableButton(ID_ViewReport, True)
        
        # Активность кнопки 'Печать отчета' 
        setResult.EnableButton(ID_PrintReport, True)
        
##################################################################################################################33

# Открываем просмотрщик

    def OnOpenViewer(self, event):
        
        """ открываем просмотрщик """
        
        frame = Viewer(None, 'Файловый просмотрщик')
        frame.Show()
    
#----------------------------------------------------------------------------------------------------------    
# Открываем окно рисования графика

    def OnPlotGraph(self, event):
        
        """ строим график """
        
        fig = PlotFrame()
        fig.Show(True)

#--------------------------------------------------------------------------------------------------------
# Открываем окно печати

    def onPrintDocument(self, event):
        
        """ выводим документ на печать """
        
        frame = PrintFrameworkSample()
        frame.Show()
    
#---------------------------------------------------------------------------------------------------------  
# Открываем окно Помощи

    def onOpenHelpWindow(self, event):
        
        """ открываем окно справки """
        
        helpwindow = HelpWindow(None)
        helpwindow.Show() 
        
##################################################################################################
#----------------------------------------- Входные данные ---------------------------------------#
##################################################################################################
# Создаем вкладки

class TabPanelOne(wx.Panel):
    
    """ Первая вкладка """
    
#--------------------------------------------------------------------------------------------
# Размещаем на панели текст и поля для ввода 

    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        # Объявляем глобальные переменные
        global txt14, txt15, txt16, txt17, txt18, txt19, txt62, txt63, txt64, impButton
               
#---- Первое поле ------- 

        """ Глубина забоя """

        # Задаем сайзеры для первого поля
        FirstSizer_vert = wx.BoxSizer(wx.VERTICAL)
        FirstSizer_hor1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Добавляем небольшой отступ сверху
        FirstSizer_vert.AddSpacer(10)
        
        # Задаем параметры шрифта
        font = wx.Font(13, wx.ROMAN, wx.ITALIC, wx.BOLD, False, u'Consolas')
        # Рисуем название поля
        text = wx.StaticText(self, wx.ID_ANY, "Для скважин с установленным УЭЦН")
        FirstSizer_vert.Add(text, flag = wx.ALIGN_CENTER)
        # Применяем шрифт
        text.SetFont(font)
        
        # Добавляем небольшой отступ сверху
        FirstSizer_vert.AddSpacer(60)
       
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor1)
        
        # Добавляем пустых строк слева
        FirstSizer_hor1.AddSpacer(20)
          
        font14 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text14 = wx.StaticText(self, wx.ID_ANY, "Глубина забоя, м")
        text14.SetFont(font14)
        text14.SetForegroundColour('black')
        self.Show(True)
        
        # Рисуем поля ввода значений
        txt14 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt14.Bind(wx.EVT_TEXT, self.onCheckFirstTabFirstField)
        
        # Устанавливаем фон поля
#         self.txt14.SetBackgroundColour("#FFFFE8")

        # Рисуем поля
        FirstSizer_hor1.Add(text14, flag = wx.ALL, border = 10)
        FirstSizer_hor1.Add(txt14, flag = wx.ALL, border = 10)
        
#------ Второе поле ----------

        """ Длина эксплуатационной колонны (с хвостовиком) """

        # Сайзер второго поля
        FirstSizer_hor2 = wx.BoxSizer(wx.HORIZONTAL)
    
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor2)
        # Добавляем пустых строк слева
        FirstSizer_hor2.AddSpacer(20)

        font15 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text15 = wx.StaticText(self, wx.ID_ANY, "Длина эксплуатационной колонны (с хвостовиком), м")
        text15.SetFont(font15)
        text15.SetForegroundColour('black')
        self.Show(True)
        
        # Рисуем поля ввода значений
        txt15 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt15.Bind(wx.EVT_TEXT, self.onCheckFirstTabSecondField)
        
        # Рисуем поля
        FirstSizer_hor2.Add(text15, flag = wx.ALL, border = 10)
        FirstSizer_hor2.Add(txt15, flag = wx.ALL, border = 10)
        
#-------- Третье поле --------

        """ Диаметр эксплуатационной колонны """

        # Сайзер третьего поля
        FirstSizer_hor3 = wx.BoxSizer(wx.HORIZONTAL)
    
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor3)
        
        # Добавляем пустых строк слева
        FirstSizer_hor3.AddSpacer(20)

        font16 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text16 = wx.StaticText(self, wx.ID_ANY, "Диаметр эксплуатационной колонны, мм")
        text16.SetFont(font16)
        text16.SetForegroundColour('black')
        self.Show(True)
        
        # Создаем поле ввода значения
        txt16 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        # Проверяем значение поля на соответствия
        txt16.Bind(wx.EVT_TEXT, self.onCheckFirstTabThirdField)
        
        FirstSizer_hor3.Add(text16, flag = wx.ALL, border = 10)
        FirstSizer_hor3.Add(txt16, flag = wx.ALL, border = 10)
        
        # Задаем отступ сверху
        FirstSizer_vert.AddSpacer(40)

#-------- Четвертое поле -----------

        """ Длина колонны НКТ """

        # Сайзер четвертого поля
        FirstSizer_hor4 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor4)
       
        # Задаем отступ слева
        FirstSizer_hor4.AddSpacer(120)

        font17 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text17 = wx.StaticText(self, wx.ID_ANY, "Длина колонны НКТ, м")
        text17.SetFont(font17)
        text17.SetForegroundColour('black')
        self.Show(True)
        
        txt17 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt17.Bind(wx.EVT_TEXT, self.onCheckFirstTabFourthField)
        
        FirstSizer_hor4.Add(text17, flag = wx.ALL, border = 10)
        FirstSizer_hor4.Add(txt17, flag = wx.ALL, border = 10)

#---------- Пятое поле --------

        """ Диаметр колонны НКТ """

        # Сайзер поля
        FirstSizer_hor5 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor5)
       
        # Задаем отступ слева
        FirstSizer_hor5.AddSpacer(120)

        font18 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text18 = wx.StaticText(self, wx.ID_ANY, "Диаметр колонны НКТ, мм")
        text18.SetFont(font18)
        text18.SetForegroundColour('black')
        self.Show(True)
        
        txt18 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt18.Bind(wx.EVT_TEXT, self.onCheckFirstTabFifthField)
        
        FirstSizer_hor5.Add(text18, flag = wx.ALL, border = 10)
        FirstSizer_hor5.Add(txt18, flag = wx.ALL, border = 10)
        
#---------- Шестое поле -------------

        """ Статический уровень флюида в скважине """

        # Сайзер поля
        FirstSizer_hor6 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor6)
       
        # Задаем отступ слева
        FirstSizer_hor6.AddSpacer(120)

        font19 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text19 = wx.StaticText(self, wx.ID_ANY, "Статический уровень флюида в скважине, м")
        text19.SetFont(font18)
        text19.SetForegroundColour('black')
        self.Show(True)
        
        txt19 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt19.Bind(wx.EVT_TEXT, self.onCheckFirstTabSixthField)
        
        FirstSizer_hor6.Add(text19, flag = wx.ALL, border = 10)
        FirstSizer_hor6.Add(txt19, flag = wx.ALL, border = 10)

#----------- Восьмое поле ----------

        """ Напряжение питания ПЭД """
    
        # Задаем отступ сверху
        FirstSizer_vert.AddSpacer(105)

        # Сайзер поля
        FirstSizer_hor8 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor8)
       
        # Задаем отступ слева
        FirstSizer_hor8.AddSpacer(220)

        font62 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text62 = wx.StaticText(self, wx.ID_ANY, "Напряжение питания ПЭД, В")
        text62.SetFont(font62)
        text62.SetForegroundColour('black')
        self.Show(True)
       
        txt62 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt62.Bind(wx.EVT_TEXT, self.onCheckFirstTabEighthField)
        
        FirstSizer_hor8.Add(text62, flag = wx.ALL, border = 10)
        FirstSizer_hor8.Add(txt62, flag = wx.ALL, border = 10)

#---------- Девятое поле ---------

        """ Частота питающего напряжения """

        # Сайзер поля
        FirstSizer_hor9 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor9)
       
        # Задаем отступ слева
        FirstSizer_hor9.AddSpacer(220)

        font63 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')  
        text63 = wx.StaticText(self, wx.ID_ANY, "Частота питающего напряжения, Гц")
        text63.SetFont(font63)
        text63.SetForegroundColour('black')
        self.Show(True)
       
        txt63 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt63.Bind(wx.EVT_TEXT, self.onCheckFirstTabNinthField)
        
        FirstSizer_hor9.Add(text63, flag = wx.ALL, border = 10)
        FirstSizer_hor9.Add(txt63, flag = wx.ALL, border = 10)

#------ Десятое поле -----------

        """ Ток потребления ПЭД """

        # Сайзер поля
        FirstSizer_hor10 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Добавляем горизонтальный сайзер в вертикальный
        FirstSizer_vert.Add(FirstSizer_hor10)
       
        # Задаем отступ слева
        FirstSizer_hor10.AddSpacer(220)

        font64 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text64 = wx.StaticText(self, wx.ID_ANY, "Ток потребления ПЭД, А")
        text64.SetFont(font64)
        text64.SetForegroundColour('black')
        self.Show(True)
        
        txt64 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt64.Bind(wx.EVT_TEXT, self.onCheckFirstTabTenthField)
        
        FirstSizer_hor10.Add(text64, flag = wx.ALL, border = 10)
        FirstSizer_hor10.Add(txt64, flag = wx.ALL, border = 10)

#--------------------------------------------------------------------------------------------------------------------                
        
        # Рисуем резделительную линию
        wx.StaticLine(self, pos=(30, 670), size=(950,2))
        
        # Рисуем кнопку 'следующая'
        self.NextFirstTabButton = wx.Button(self, wx.ID_OK, label="следующая>", pos=(500, 700))
       
        # Рисуем кнопку закрыть
        self.CloseFirstTabButton = wx.Button(self, wx.ID_OK, label="Закрыть", pos=(650, 700))
      
         # Рисуем кнопку для импорта данных
        impButton = wx.Button(self, wx.ID_OK, label="Загрузить данные", pos=(50, 700))
        
        
        # Переключаемся на другую вкладку по нажатию кнопки
        self.NextFirstTabButton.Bind(wx.EVT_BUTTON, self.OnCheckFirstTab, self.NextFirstTabButton)
        
        # При нажатии закрываем окно
        self.CloseFirstTabButton.Bind(wx.EVT_BUTTON, self.onCloseDataTabOne, self.CloseFirstTabButton)
        
        # Вызываем импорт данных
        impButton.Bind(wx.EVT_BUTTON, self.onLoadData, impButton)
        
        """
             после проверки заполнения всех полей на первой вкладке (в случае заполнения всех пустых полей)
            переходим к заполнению полей следующей вкладки
            
        """
        self.SetSizer(FirstSizer_vert)
        self.Layout()

#-----------------------------------------------------------------------------------------------------------------
    def onLoadData(self, event):
        
        """ загружаем в редактор ранее сохраненные данные """
        
         # Считываем данные из файла
        wildcard = "Text source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
    
        self.currentDirectory = os.getcwd()

        dlg = wx.FileDialog(self, message="Открытие документа", defaultDir=self.currentDirectory, 
                            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            
            path = dlg.GetPath()
            
            report = open(path, "r") 
            
        data_load = report.readlines()
            
        report.close()
 
        # удаляем строки заголовка с 1 по 18 строку 
        del data_load[0:15]
        
        # преобразуем list в string (объединяем все значения в один список)
        value = "".join(data_load)
    
        # разделяем список на части
        devOne = value.split()

        # удаляем весь лишний текст до первого значения
        del devOne[:3]

        # присваиваем значение переменным
        valueOne = devOne[0]
        valueTwo = devOne[7]
        valueThree = devOne[11]
        valueFour = devOne[16]
        valueFive = devOne[21]
        valueSix = devOne[28]
        valueSeven = devOne[35]
        valueEight = devOne[40]
        valueNine = devOne[48]
        valueTen = devOne[56]

        valueEleven = devOne[65]
        valueTwelve = devOne[73]
        valueThirteen = devOne[80]
        valueFourteen = devOne[85]
        valueFifteen = devOne[90]
        valueSixteen = devOne[99]
        valueSeventeen = devOne[104]
        valueEighteen = devOne[108]
        valueNineteen = devOne[116]
        valueTwenty = devOne[122]
        
        valueTwentyOne = devOne[127]
        valueTwentyTwo = devOne[136]
        valueTwentyThree = devOne[142]
        valueTwentyFour = devOne[150]
        valueTwentyFive = devOne[159]
        valueTwentySix = devOne[167]
        valueTwentySeven = devOne[172]
        valueTwentyEight = devOne[178]
        valueTwentyNine = devOne[184]
        valueThirty = devOne[191]

        valueThirtyOne = devOne[197] 
        valueThirtyTwo = devOne[204]
        valueThirtyThree = devOne[210] 
        valueThirtyFour = devOne[215]
        valueThirtyFive = devOne[220]
        valueThirtySix = devOne[231]
        valueThirtySeven = devOne[236]
        valueThirtyEight = devOne[241]
        valueThirtyNine = devOne[246]
        valueForty = devOne[251]

        valueFortyOne = devOne[256]
        valueFortyTwo = devOne[260]
        valueFortyThree = devOne[271]
        valueFortyFour = devOne[276]
        valueFortyFive = devOne[282]
        valueFortySix = devOne[288]
        valueFortySeven = devOne[296]
        valueFortyEight = devOne[304]
        valueFortyNine = devOne[308]
        valueFifty = devOne[314]

        valueFiftyOne = devOne[321]

        # преобразуем полученное значение в число
        num1 = float(valueOne)
        num2 = float(valueTwo)
        num3 = float(valueThree)
        num4 = float(valueFour)
        num5 = float(valueFive)
        num6 = float(valueSix)
        num7 = float(valueSeven)
        num8 = float(valueEight)
        num9 = float(valueNine)
        num10 = float(valueTen)
        
        num11 = float(valueEleven)
        num12 = float(valueTwelve)
        num13 = float(valueThirteen)
        num14 = float(valueFourteen)
        num15 = float(valueFifteen)
        num16 = float(valueSixteen)
        num17 = float(valueSeventeen)
        num18 = float(valueEighteen)
        num19 = float(valueNineteen)
        num20 = float(valueTwenty)
        
        num21 = float(valueTwentyOne)
        num22 = float(valueTwentyTwo)
        num23 = float(valueTwentyThree)
        num24 = float(valueTwentyFour)
        num25 = float(valueTwentyFive)
        num26 = float(valueTwentySix)
        num27 = float(valueTwentySeven)
        num28 = float(valueTwentyEight)
        num29 = float(valueTwentyNine)
        num30 = float(valueThirty)
        
        num31 = float(valueThirtyOne)
        num32 = float(valueThirtyTwo)
        num33 = float(valueThirtyThree)
        num34 = float(valueThirtyFour)
        num35 = float(valueThirtyFive)
        num36 = float(valueThirtySix)
        num37 = float(valueThirtySeven)
        num38 = float(valueThirtyEight)
        num39 = float(valueThirtyNine)
        num40 = float(valueForty)
        
        num41 = float(valueFortyOne)
        num42 = float(valueFortyTwo)
        num43 = float(valueFortyThree)
        num44 = float(valueFortyFour)
        num45 = float(valueFortyFive)
        num46 = float(valueFortySix)
        num47 = float(valueFortySeven)
        num48 = float(valueFortyEight)
        num49 = float(valueFortyNine)
        
        num50 = float(valueFifty)
        num51 = float(valueFiftyOne)
       
        # записываем результат в промежуточный файл
        
        path = "Data\Temporary\Treated_Data.txt"
        f = open(path, "w") 
        f.write(str(num1) + "\n")
        f.write(str(num2) + "\n")
        f.write(str(num3) + "\n")
        f.write(str(num4) + "\n")
        f.write(str(num5) + "\n")
        f.write(str(num6) + "\n")
        f.write(str(num7) + "\n")
        f.write(str(num8) + "\n")
        f.write(str(num9) + "\n")
        f.write(str(num10) + "\n")
        
        f.write(str(num11) + "\n")
        f.write(str(num12) + "\n")
        f.write(str(num13) + "\n")
        f.write(str(num14) + "\n")
        f.write(str(num15) + "\n")
        f.write(str(num16) + "\n")
        f.write(str(num17) + "\n")
        f.write(str(num18) + "\n")
        f.write(str(num19) + "\n")
        f.write(str(num20) + "\n")
        
        f.write(str(num21) + "\n")
        f.write(str(num22) + "\n")
        f.write(str(num23) + "\n")
        f.write(str(num24) + "\n")
        f.write(str(num25) + "\n")
        f.write(str(num26) + "\n")
        f.write(str(num27) + "\n")
        f.write(str(num28) + "\n")
        f.write(str(num29) + "\n")
        f.write(str(num30) + "\n")
        
        f.write(str(num31) + "\n")
        f.write(str(num32) + "\n")
        f.write(str(num33) + "\n")
        f.write(str(num34) + "\n")
        f.write(str(num35) + "\n")
        f.write(str(num36) + "\n")
        f.write(str(num37) + "\n")
        f.write(str(num38) + "\n")
        f.write(str(num39) + "\n")
        f.write(str(num40) + "\n")
        
        f.write(str(num41) + "\n")
        f.write(str(num42) + "\n")
        f.write(str(num43) + "\n")
        f.write(str(num44) + "\n")
        f.write(str(num45) + "\n")
        f.write(str(num46) + "\n")
        f.write(str(num47) + "\n")
        f.write(str(num48) + "\n")
        f.write(str(num49) + "\n")
        f.write(str(num50) + "\n") 
        f.write(str(num51)) 
        f.close()

        # Считываем данные из промежуточного файла и присваиваем значения переменным,
        #                которые будут участвовать в расчете 

        # задаем расположение файла
        filename="Data\Temporary\Treated_Data.txt"

        # считываем данные из файла
        with open (filename, "r") as myfile:
            data=myfile.readlines()

        # Присваиваем значения переменным, которые будут участвовать в расчете
        
 #---------- Данные первой вкладки -----------#
        
        h_bhole = data[0]
        h_obs = data[1]
        d_vnesh_obs = data[2]
        h_nkt = data[3] 
        d_vnesh_nkt = data[4]
        h_stat = data[5]
        u_ESP = data[36]
        f_ESP = data[37]
        i_ESP = data[38]

#  --------- Данные второй вкладки ----------#

        t_bhole = data[6]
        h_ice = data[7]
        t_month = data[8] 
        t_maxh = data[9] 

#  -------- Данные третьей вкладки -----------#

        ro  = data[10]
        visc_plast = data[11]
        pn_plast = data[12]
        tkpn = data[13]
        g_plast = data[14]

#  -------- Данные четвертой вкладки ----------#

        nomdebit = data[15]
        debit_oil = data[16]  
        g = data[17]
        water = data[18]
        h_din = data[19]
        p_wellhead = data[20]
        t_wellhead = data[21]
        debit = data[22]
        scraper = data[23]
        h_aspo = data[24]

#-------- Данные пятой вкладки -------#

        ro_oil = data[25] 
        visc_oil = data[26]
        cp = data[27]
        asf = data[28]
        silica_gel = data[29]
        freezing_oil = data[30]
        t_0 = data[31]
        melting = data[32]
        ro_gas = data[33]
        ro_water = data[34]
        
 #-------- Данные шестой вкладки ---------#

        ESP_gas = data[35]
        d_vnut_nkt = data[39]
        d_vnut_obs = data[40]
        c_neft = data[41]
        kll = data[42]
        holkon = data[43]
        sh_gr = data[44]
        glub_zap = data[45]
        min_T_zap = data[46]
        ustavka = data[47]
        d_kab = data[48]
        long_ = data[49]
        u_u = data[50]
        
        # вставляем данные в соответствующие поля
        number1 = str(txt14.SetValue(h_bhole))
        number2 = str(txt15.SetValue(h_obs))
        number3 = str(txt16.SetValue(d_vnesh_obs))
        number4 = str(txt17.SetValue(h_nkt))
        number5 = str(txt18.SetValue(d_vnesh_nkt))
        number6 = str(txt19.SetValue(h_stat))
        number7 = str(txt62.SetValue(u_ESP))
        number8 = str(txt63.SetValue(f_ESP))
        number9 = str(txt64.SetValue(i_ESP))
        
        number10 = str(txt21.SetValue(t_bhole))
        number11 = str(txt22.SetValue(h_ice))
        number12 = str(txt23.SetValue(t_month))
        number13 = str(txt24.SetValue(t_maxh))
        
        number14 = str(txt31.SetValue(ro))
        number15 = str(txt32.SetValue(visc_plast))
        number16 = str(txt33.SetValue(pn_plast))
        number17 = str(txt34.SetValue(tkpn))
        number18 = str(txt35.SetValue(g_plast))
        
        number19 = str(txt41.SetValue(nomdebit))
        number20 = str(txt42.SetValue(debit_oil))
        number21 = str(txt43.SetValue(g))
        number22 = str(txt44.SetValue(water))
        number23 = str(txt45.SetValue(h_din))
        number24 = str(txt46.SetValue(p_wellhead))
        number25 = str(txt47.SetValue(t_wellhead))
        number26 = str(txt48.SetValue(debit))
        number27 = str(txt49.SetValue(scraper))
        number28 = str(txt410.SetValue(h_aspo))
        
        number29 = str(txt51.SetValue(ro_oil))
        number30 = str(txt52.SetValue(visc_oil))
        number31 = str(txt53.SetValue(cp))
        number32 = str(txt54.SetValue(asf))
        number33 = str(txt55.SetValue(silica_gel))
        number34 = str(txt56.SetValue(freezing_oil))
        number35 = str(txt57.SetValue(t_0))
        number36 = str(txt58.SetValue(melting))
        number37 = str(txt59.SetValue(ro_gas))
        number38 = str(txt510.SetValue(ro_water))
        
        number39 = str(txt61.SetValue(ESP_gas))
        number40 = str(txt65.SetValue(d_vnut_nkt))
        number41 = str(txt66.SetValue(d_vnut_obs))
        number42 = str(txt67.SetValue(c_neft))
        number43 = str(txt68.SetValue(kll))
        number44 = str(txt69.SetValue(holkon))
        number45 = str(txt610.SetValue(sh_gr))
        number46 = str(txt611.SetValue(glub_zap))
        number47 = str(txt612.SetValue(min_T_zap))
        number48 = str(txt613.SetValue(ustavka))
        number49 = str(txt614.SetValue(d_kab))
        number50 = str(txt615.SetValue(long_))
        number51 = str(txt616.SetValue(u_u))
            
        # Выводим сообщение
        wx.MessageBox('Данные успешно загружены!', 'Сообщение', wx.OK | wx.ICON_INFORMATION)
#----------------------------------------------------------------------------------------------------------------        
# Закрываем окно 

    def onCloseDataTabOne(self, event):
        
        """ Закрываем ноутбук с данными """      
  
        self.GetTopLevelParent().Destroy()
    
#---------------------------------------------------------------------------------------------------------------

# Проверяем заполнение всех поей вкладки

    def OnCheckFirstTab(self, event):
        
        """ проверяем полноту заполнение полей первой вкладки """
             
        # Контрольные значения
        OnePointFour = txt14.GetValue()
        OnePointFive = txt15.GetValue()
        OnePoinSix = txt16.GetValue()
        OnePoinSeven = txt17.GetValue()
        OnePoinEight = txt18.GetValue()
        OnePoinNine = txt19.GetValue()
        SixPointTwo = txt62.GetValue()
        SixPointThree = txt63.GetValue()
        SixPointFour = txt64.GetValue()
        
        if OnePointFour and OnePointFive and OnePoinSix and OnePoinSeven and OnePoinEight and OnePoinNine and SixPointTwo and SixPointThree and SixPointFour != '':
            
            # Переходим на следующую вкладку
            self.notebook = self.GetParent()
            self.notebook.SetSelection(1)
            
            # Если все поля заполнены - делаем кнопку 'следующая' неактивной
            self.NextFirstTabButton.Enable()
           
        else:
            # если все иначе - выводим сообщение
            wx.MessageBox(u'Чтобы перейти к следующей вкладке, пожалуйста, заполните все пустые поля', 'Ошибка ввода данных', wx.OK | wx.ICON_ERROR)
            
# ------------ Проверка введенных значение на соответствие --------------------------- 

    def onCheckFirstTabFirstField(self, event):
        
        """ Проверяем первое поле. 1.4 Глубина забоя. """
        
        # Значение поля равно
        OnePointFour = txt14.GetValue() # глубина забоя
        
        # Делаем проверку
        if OnePointFour == '':
            txt14.SetToolTip(wx.ToolTip("введите значение"))
        else: 
            # делаем тип string
            h_bhole = str(OnePointFour) 
            
            # проверка на отрицательность значения поля
            if h_bhole < '0':
                # раскрашиваем значение красным если отрицательное
                txt14.SetForegroundColour(wx.RED)
                txt14.Refresh()
                # Выводим предупреждающую надпись    
                txt14.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение глубины забоя")) 
            else:
                # делаем тип float
                h_bhole = float(OnePointFour)                
                # усли больше нуля
                if h_bhole >= 0 and h_bhole <= 5000:
                    # Делаем шрифт черным
                    txt14.SetForegroundColour(wx.BLACK)
                    txt14.Refresh()
                    # Выводим предупреждающую надпись    
                    txt14.SetToolTip(wx.ToolTip(""))
                else:
                    # Меняем шрифт на красный
                    txt14.SetForegroundColour(wx.RED)
                    txt14.Refresh()
                    # Выводим предупреждающую надпись    
                    txt14.SetToolTip(wx.ToolTip("Внимание ошибка! Значение глубины забоя находится вне допустимого диапазона"))
#------------------------------------------------------------------------------------------------

    def onCheckFirstTabSecondField(self, event):
        
        """ Проверяем второе поле. 1.5 Длина эксплуатационной колонны. """
        
        # Значение поля равно
        OnePointFive = txt15.GetValue()
        OnePointFour = txt14.GetValue()
       
        # Делаем проверку
        if OnePointFive == '':
            txt15.SetToolTip(wx.ToolTip("введите значение"))
        else:
            h_obs = str(OnePointFive)   # длина эксплуатационной колонны 
            h_bhole = str(OnePointFour) # глубина забоя
            
            if h_obs < '0' :
                txt15.SetForegroundColour(wx.RED)
                txt15.Refresh()
                # Выводим предупреждающую надпись    
                txt15.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение длины")) 
            else:
                h_obs = float(OnePointFive)
                h_bhole = float(OnePointFour)
                
                # Глубина эксплуатационной колонны должна быть больше глубины забоя
                if h_obs > 0 and h_obs >= h_bhole:
                    txt15.SetForegroundColour(wx.BLACK) 
                    txt15.Refresh()
                    txt15.SetToolTip(wx.ToolTip(""))                                                                    
                else:
                    txt15.SetForegroundColour(wx.RED)
                    txt15.Refresh()
                    txt15.SetToolTip(wx.ToolTip("Внимание ошибка! Необходимы данные инклинометрии"))                       

#------------------------------------------------------------------------------------------------
  
    def onCheckFirstTabThirdField(self, event):
        
        """ Проверяем третье поле. 1.6 Диаметр эксплуатационной колонны. """
        
        # Значение поля равно
        OnePoinSix = txt16.GetValue() # диаметр эксплуатационной колонны
               
        # Делаем проверку
        if OnePoinSix == '':
            txt16.SetToolTip(wx.ToolTip(""))
        else:
            h_obs = str(OnePoinSix)
        
            if h_obs < '0':
                txt16.SetForegroundColour(wx.RED)
                txt16.Refresh()
                # Выводим предупреждающую надпись    
                txt16.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение диаметра")) 
            else:
                h_obs = float(OnePoinSix)
                
                if h_obs >= 140 and h_obs <= 180:
                    txt16.SetForegroundColour(wx.BLACK)
                    txt16.Refresh()
                    # Выводим предупреждающую надпись    
                    txt16.SetToolTip(wx.ToolTip(""))
                else:
                    txt16.SetForegroundColour(wx.RED)
                    txt16.Refresh()
                    # Выводим предупреждающую надпись    
                    txt16.SetToolTip(wx.ToolTip("Внимание ошибка! Значение диаметра находится вне допустимого диапазона"))
                    
#---------------------------------------------------------------------------------------------------------
# Четвертое поле

    def onCheckFirstTabFourthField(self, event):
        
        """ Проверяем четвертое поле. 1.7 Длина колонны НКТ. """
        
        # Значение поля равно
        OnePoinFive = txt15.GetValue() # длина эксплуатационной колонны
        OnePoinSeven = txt17.GetValue() # длина колонны НКТ
        
        
        # Делаем проверку
        if OnePoinSeven == '':
            txt17.SetToolTip(wx.ToolTip(""))
        else:
            h_nkt = str(OnePoinSeven) # длина колонны НКТ
            h_obs = str(OnePoinFive)  # длина эксплуатационной колонны (обсадная колонна)
       
            if h_nkt < '0':
                txt17.SetForegroundColour(wx.RED)
                txt17.Refresh()
                # Выводим предупреждающую надпись    
                txt17.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение диаметра")) 
            else:
                h_nkt = float(OnePoinSeven)
                h_obs = float(OnePoinFive)
                
                if OnePoinFive > 0 and OnePoinSeven < OnePoinFive:
            
                    # Если значение в диапазоне, задаем черный цвет значения
                    txt17.SetForegroundColour(wx.BLACK)
                    txt17.Refresh()
                    txt17.SetToolTip(wx.ToolTip(""))
            
                else:
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt17.SetForegroundColour(wx.RED)
                    txt17.Refresh()
                    # Выводим предупреждающую надпись    
                    txt17.SetToolTip(wx.ToolTip("Внимание ошибка! Длина НКТ больше длины обсадной колонны"))
            
#------------------------------------------------------------------------------------------------------------------------
# Пятое поле

    def onCheckFirstTabFifthField(self, event):
        
        """ Проверяем пятое поле. 1.8 Диаметр колонны НКТ """
        
        # Значение поля равно
        OnePoinEight = txt18.GetValue()  # диаметр колонны НКТ
        OnePointSix = txt16.GetValue() # диаметр обсадной уолонны
        
        # Делаем проверку
        if OnePoinEight == '':
            txt18.SetToolTip(wx.ToolTip(""))
        else:
            d_vnesh_nkt = str(OnePoinEight) # диаметр колонны НКТ
            
            if d_vnesh_nkt < '0':
                # Если значение не в диапазоне, задаем красный цвет значения
                txt18.SetForegroundColour(wx.RED)
                txt18.Refresh()
                # Выводим предупреждающую надпись    
                txt18.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение диаметра НКТ"))
            else:
                d_vnesh_nkt = float(OnePoinEight)
                d_vnesh_obs = float(OnePointSix)
        
                if d_vnesh_nkt > 0 and d_vnesh_nkt < d_vnesh_obs:
                    # Если значение в диапазоне, задаем черный цвет значения
                    txt18.SetForegroundColour(wx.BLACK)
                    txt18.Refresh()
                    txt18.SetToolTip(wx.ToolTip(""))
                else:
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt18.SetForegroundColour(wx.RED)
                    txt18.Refresh()
                    # Выводим предупреждающую надпись    
                    txt18.SetToolTip(wx.ToolTip("Внимание ошибка! Значение диаметра НКТ находится вне допустимого диапазона"))
#---------------------------------------------------------------------------------------------------------
# Шестое поле
    
    def onCheckFirstTabSixthField(self, event):
 
        """ Проверяем шестое поле. 1.9 Статический уровень флюида в скважине """
        
        # 
        OnePoinNine  = txt19.GetValue()
        
        # Делаем проверку
        if OnePoinNine == '':
            txt19.SetToolTip(wx.ToolTip("введите значение"))
        else: 
            h_stat = str(OnePoinNine)
            
            if h_stat < '0':
                txt19.SetForegroundColour(wx.RED)
                txt19.Refresh()
                # Выводим предупреждающую надпись    
                txt19.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение статического уровня")) 
            else:
                h_stat = float(OnePoinNine)
                
                if h_stat >= 0:
                    txt19.SetForegroundColour(wx.BLACK)
                    txt19.Refresh()
                    # Выводим предупреждающую надпись    
                    txt19.SetToolTip(wx.ToolTip(""))
                else:
                    txt19.SetForegroundColour(wx.RED)
                    txt19.Refresh()
                    # Выводим предупреждающую надпись    
                    txt19.SetToolTip(wx.ToolTip("Внимание ошибка! Значение статического уровня находится вне допустимого диапазона")) 
#---------------------------------------------------------------------------------------------------------------------------------            
# Седьмое поле 
    
#     def onCheckFirstTabSeventhField(self, event):
        
#         """ Проверяем седьмое поле. add Толщина стенки НКТ. """
        
#         # Значение поля равно
#         AdditionalField = add.GetValue()
        
#         # Делаем проверку
#         if AdditionalField == '':
#             add.SetToolTip(wx.ToolTip("введите значение"))
            
#         else: 
#             value = str(AdditionalField)
            
#             if value < '0':
#                 add.SetForegroundColour(wx.RED)
#                 add.Refresh()
#                 # Выводим предупреждающую надпись    
#                 add.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение толщины"))       
        
#             else:
#                 value = float(AdditionalField)
            
#                 if value >= 0 and value >= 5 and value <= 6:
#                     # Если значение в диапазоне, задаем черный цвет значения
#                     add.SetForegroundColour(wx.BLACK)
#                     add.Refresh()
#                     add.SetToolTip(wx.ToolTip(""))
#                 else:
#                     # Если значение не в диапазоне, задаем красный цвет значения
#                     add.SetForegroundColour(wx.RED)
#                     add.Refresh()
#                     # Выводим предупреждающую надпись    
#                     add.SetToolTip(wx.ToolTip("Внимание ошибка! Значение толщины находится вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------
# Восьмое поле 

    def onCheckFirstTabEighthField(self, event):
        
        """ Проверяем восьмое поле. 6.2 Напряжение питания ПЭД. """
        
        # Значение поля равно
        SixPointTwo = txt62.GetValue()
        
        # Делаем проверку
        if SixPointTwo == '':
            txt62.SetToolTip(wx.ToolTip("введите значение"))
            
        else:
            u_ESP = str(SixPointTwo)
            if u_ESP < '0':
                txt62.SetForegroundColour(wx.RED)
                txt62.Refresh()
                # Выводим предупреждающую надпись    
                txt62.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение напряжения"))                
            
            else:
                u_ESP = float(SixPointTwo)
        
                if u_ESP >= 0 and u_ESP < 3500 and u_ESP > 600:
                    txt62.SetForegroundColour(wx.BLACK)
                    txt62.Refresh()
                    txt62.SetToolTip(wx.ToolTip(""))
                
                elif u_ESP < 600: 
                    txt62.SetForegroundColour(wx.RED)
                    txt62.Refresh()
                    # Выводим предупреждающую надпись    
                    txt62.SetToolTip(wx.ToolTip("Внимание ошибка! Значение напряжения находится вне допустимого диапазона"))
      
                else:
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt62.SetForegroundColour(wx.RED)
                    txt62.Refresh()
                    # Выводим предупреждающую надпись    
                    txt62.SetToolTip(wx.ToolTip("Внимание ошибка! Значение напряжения находится вне допустимого диапазона"))
#------------------------------------------------------------------------------------------------------------
# Девятое поле 

    def onCheckFirstTabNinthField(self, event):
        
        """ Проверяем девятое поле. 6.3 Частота питающего напряжения. """
        
        # Значение поля равно
        SixPointThree = txt63.GetValue()
        
        # Делаем проверку
        if SixPointThree == '':
            txt63.SetToolTip(wx.ToolTip("введите значение"))
            
        else:
            f_ESP = str(SixPointThree)
            # Проверка на отрицательность значения
            if f_ESP < '0':
                txt63.SetForegroundColour(wx.RED)
                txt63.Refresh()
                # Выводим предупреждающую надпись    
                txt63.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение частоты")) 
           
            else:
                f_ESP = float(SixPointThree)
    
                if f_ESP >= 0 and f_ESP > 40 and f_ESP < 60:
            
                    # Если значение в диапазоне, задаем черный цвет значения
                    txt63.SetForegroundColour(wx.BLACK)
                    txt63.Refresh()
                    txt63.SetToolTip(wx.ToolTip(""))
            
                elif f_ESP > 60:
                    txt63.SetForegroundColour(wx.RED)
                    txt63.Refresh() 
                    txt63.SetToolTip(wx.ToolTip("Внимание ошибка! Значение частоты находится вне допустимого диапазона"))
                else:
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt63.SetForegroundColour(wx.RED)
                    txt63.Refresh()
                    # Выводим предупреждающую надпись    
                    txt63.SetToolTip(wx.ToolTip("Внимание ошибка! Значение частоты находится вне допустимого диапазона"))
#----------------------------------------------------------------------------------------------------------
# Десятое поле 

    def onCheckFirstTabTenthField(self, event):
        
        """ Проверяем десятое поле. 6.4 Ток потребления ПЭД. """
        
        # Значение поля равно
        SixPointFour = txt64.GetValue()        
        
        # Делаем проверку
        if SixPointFour  == '':            
            txt64.SetToolTip(wx.ToolTip("введите значение"))
        else:
            i_ESP = str(SixPointFour) # меняем тип с float на string (работа с отрицательными значениями)
            
            # Проверка на отрицательность значения
            if i_ESP < '0':
                txt64.SetForegroundColour(wx.RED)
                txt64.Refresh()
                # Выводим предупреждающую надпись    
                txt64.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение тока")) 
    
            else:
                # Делаем тип данных float
                i_ESP = float(SixPointFour)
                
                # Проверяем на условия
                if i_ESP > 0 and i_ESP < 100 and i_ESP > 10:
                    txt64.SetForegroundColour(wx.BLACK)
                    txt64.Refresh()
                    txt64.SetToolTip(wx.ToolTip(""))
            
                elif i_ESP < 100:    
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt64.SetForegroundColour(wx.RED)
                    txt64.Refresh()
                    # Выводим предупреждающую надпись    
                    txt64.SetToolTip(wx.ToolTip("Внимание ошибка! Значение тока находится вне допустимого диапазона"))
       
                else:
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt64.SetForegroundColour(wx.RED)
                    txt64.Refresh()
                    # Выводим предупреждающую надпись    
                    txt64.SetToolTip(wx.ToolTip("Внимание ошибка! Значение тока находится вне допустимого диапазона"))

########################################################################
class TabPanelTwo(wx.Panel):
    """
    Вторая вкладка 
    
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        
        """  """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        # Объявляем глобальные переменные
        global txt21, txt22, txt23, txt24
        
# ------- Первое поле -----------
        """ Температура нефтяного пласта """

        # Задаем сайзеры (вертикальный и горизонтальный)
        SecondSizer_vert = wx.BoxSizer(wx.VERTICAL)
        SecondSizer_horiz1 = wx.BoxSizer(wx.HORIZONTAL) 
        
        # Добавляем пустых строк сверху и пробелов слева
        SecondSizer_vert.AddSpacer(60)
        SecondSizer_horiz1.AddSpacer(100)
        
        # Размещаем горизонтальный сайзер в вертикальном (название поля и его значение в одной строке)
        SecondSizer_vert.Add (SecondSizer_horiz1)
        
        font21 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text21 = wx.StaticText(self, wx.ID_ANY, "Температура нефтяного пласта, град. С")
        text21.SetFont(font21)
        text21.SetForegroundColour('black')
        self.Show(True)
       
        # Рисуем поле со значением
        txt21 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        # Обрабатываем событие
        txt21.Bind(wx.EVT_TEXT, self.onCheckSecondTabFirstField)
        
        # Задаем дистанцию между текстом и полем 
        SecondSizer_horiz1.Add(text21, flag = wx.ALL, border = 10)
        SecondSizer_horiz1.Add(txt21, flag = wx.ALL, border = 10)
        
#------- Второе поле ---------
        
        """ Глубина вечномерзлых грунтов """
        
        # Задаем сайзер 
        SecondSizer_horiz2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Размещаем горизонтальный сайзер в вертикальном
        SecondSizer_vert.Add (SecondSizer_horiz2)
        
        # Добавляем пробелов
        SecondSizer_horiz2.AddSpacer(100)
              
        # Задаем параметры шрифта
        font22 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas') 
        # Выводим название пункта
        text22 = wx.StaticText(self, wx.ID_ANY, "Глубина вечномерзлых грунтов, м")
        # Устанавливаем шрифт
        text22.SetFont(font22)
        # Задаем цвет шрифта
        text22.SetForegroundColour('black')
        # Делаем надпись видимой
        self.Show(True)
        
        # Выводим поле значения
        txt22 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        # Обрабатываем событие
        txt22.Bind(wx.EVT_TEXT, self.onCheckSecondTabSecondField)
   
        # Задаем дистанцию между текстом и полем 
        SecondSizer_horiz2.Add(text22, flag = wx.ALL, border = 10)
        SecondSizer_horiz2.Add(txt22, flag = wx.ALL, border = 10)
    
# ----- Третье поле ---------
        
        """ Средняя температура наиболее холодного месяца """
        
        # Задаем сайзер для расстояния между строк
        SecondSizer_horiz3 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Размещаем горизонтальный сайзер в вертикальном
        SecondSizer_vert.Add (SecondSizer_horiz3)
             
        # Добавляем пробелов
        SecondSizer_horiz3.AddSpacer(100)
       
        # Задаем параметры шрифта
        font23 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        # Выводим название пункта
        text23 = wx.StaticText(self, wx.ID_ANY, "Средняя температура наиболее холодного месяца, град. С")
        # Устанавливаем шрифт
        text23.SetFont(font23)
        
        text23.SetForegroundColour('black')
        self.Show(True)
    
        # Рисуем поле для ввода
        txt23 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        # Обрабатываем событие
        txt23.Bind(wx.EVT_TEXT, self.onCheckSecondTabThirdField)
        
        # Расстояние между текстом и полем
        SecondSizer_horiz3.Add(text23, flag = wx.ALL, border = 10)
        SecondSizer_horiz3.Add(txt23, flag = wx.ALL, border = 10)
        
# ---- Четвертое поле -----
        
        """ Максимальная температура наиболее теплого месяца """

        # Интервал между вторым и третьим полем 
        SecondSizer_horiz4 = wx.BoxSizer(wx.HORIZONTAL)
        
        SecondSizer_vert.Add (SecondSizer_horiz4)
        
        # Добавляем слева пустых строк
        SecondSizer_horiz4.AddSpacer(100)

        font24 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text24 = wx.StaticText(self, wx.ID_ANY, "Максимальная температура наиболее теплого месяца, град. С")
        text24.SetFont(font24)
        text24.SetForegroundColour('black')
        self.Show(True)
       
        txt24 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt24.Bind(wx.EVT_TEXT, self.onCheckSecondTabFourthField)
      
        # Расстояние между названием и полем
        SecondSizer_horiz4.Add(text24, flag = wx.ALL, border = 10)
        SecondSizer_horiz4.Add(txt24, flag = wx.ALL, border = 10)
        
        StaticLine = wx.StaticLine(self, pos=(30, 270), size=(950,2))

#------- Кнопки --------
          
        self.NextSecondTabButton = wx.Button(self, wx.ID_OK, label="следующая>", pos=(500, 700))
        
        self.NextSecondTabButton.Bind(wx.EVT_BUTTON, self.OnCheckSecondTab, self.NextSecondTabButton)
    
    
        self.CloseSecondTabButton = wx.Button(self, wx.ID_OK, label="Закрыть", pos=(650, 700))
        
        self.CloseSecondTabButton.Bind(wx.EVT_BUTTON, self.onCloseDataTabTwo, self.CloseSecondTabButton)
        
        
        self.SetSizer(SecondSizer_vert)
        self.Layout()
#-----------------------------------------------------------------------------------------------------------------        
# Закрываем окно ноутбука

    def onCloseDataTabTwo(self, event):
        """ Закрываем ноутбук с данными """      
  
        self.GetTopLevelParent().Destroy()
    
#-----------------------------------------------------------------------------------------------------------------

# Переходим на третью вкладку
    def OnCheckSecondTab(self, event):
        
        # Контрольные значения
        TwoPointOne = txt21.GetValue()
        TwoPointTwo = txt22.GetValue()
        TwoPointThree = txt23.GetValue()
        TwoPointFour = txt24.GetValue()
        
        if TwoPointOne and TwoPointTwo and TwoPointThree and TwoPointFour != '':
            
            # Переходим на следующую вкладку
            self.notebook = self.GetParent()
            self.notebook.SetSelection(2)
            
            # Если все поля заполнены - делаем кнопку 'следующая' неактивной
            self.NextSecondTabButton.Enable()
            
             # Делаем вкладку неактивной
#             self.notebook.EnableTab(1, False)
        else:
            # Выводим сообщение
            wx.MessageBox(u'Чтобы перейти к следующей вкладке, пожалуйста, заполните все пустые поля', 'Ошибка ввода данных', wx.OK | wx.ICON_ERROR)
            
#-----------------------------------------------------------------------------------------------------------------
# Проверка первого поля

    def onCheckSecondTabFirstField(self, event):
        
        """ Проверяем первое поле. 2.1 Температура нефтяного пласта. """      
        
        # Задаем значения
        TwoPointOne = txt21.GetValue() # температура нефтяного пласта
        OnePointFour = txt14.GetValue()    # злубина забоя
        
        # Делаем проверку на отрицательность
        if TwoPointOne == '':
            txt21.SetToolTip(wx.ToolTip("введите значение"))
        else:
            t_bhole = str(TwoPointOne)
            # Проверка на отрицательность значения
            if t_bhole < '0':
                txt21.SetForegroundColour(wx.RED)
                txt21.Refresh()
                # Выводим предупреждающую надпись    
                txt21.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение температуры"))     
            else:
                # Делаем тип данных float
                t_bhole = float(TwoPointOne)
                h_bhole = float(OnePointFour)
     
                if t_bhole >= 0 and t_bhole > (0.01 * h_bhole) and t_bhole < (0.03 * h_bhole):
            
                    # Если значение в диапазоне, задаем черный цвет значения
                    txt21.SetForegroundColour(wx.BLACK)
                    txt21.Refresh()
                    txt21.SetToolTip(wx.ToolTip(""))
                else:            
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt21.SetForegroundColour(wx.RED)
                    txt21.Refresh()
                    # Выводим предупреждающую надпись    
                    txt21.SetToolTip(wx.ToolTip("Внимание ошибка! Значение находится вне допустимого диапазона"))
            
#-----------------------------------------------------------------------------------------------------------------
# Проверка второго поля            

    def onCheckSecondTabSecondField(self, event):
        
        """ Проверяем второе поле. 2.2 Глубина вечномерзлых грунтов. """  
        
        # Задаем значения
        TwoPointTwo = txt22.GetValue() # температура нефтяного пласта
        
        # Делаем проверку на отрицательность
        if TwoPointTwo == '':
            txt22.SetToolTip(wx.ToolTip("введите значение"))
        else:
            h_ice = str(TwoPointTwo)
            # Проверка на отрицательность значения
            if h_ice < '0':
                txt22.SetForegroundColour(wx.RED)
                txt22.Refresh()
                # Выводим предупреждающую надпись    
                txt22.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение глубины"))  
            else:
                h_ice = float(TwoPointTwo)
                
                if h_ice >= 0:
                    # Если значение в диапазоне, задаем черный цвет значения
                    txt22.SetForegroundColour(wx.BLACK)
                    txt22.Refresh()
                    txt22.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------
# Проверка третьего поля    

    def onCheckSecondTabThirdField(self, event):
        
        """ Проверяем третье поле. 2.3 Средняя температура наиболее холодного месяца. """ 
        
        # Задаем значения
        TwoPointThree = txt23.GetValue() # cредняя температура наиболее холодного месяца
        
        # Делаем проверку на отрицательность
        if TwoPointThree == '':
            txt23.SetToolTip(wx.ToolTip("введите значение"))
        else:
            t_month = str(TwoPointThree)
            
            # Проверка на отрицательность значения
            if t_month < '0':
                # Если значение в диапазоне, задаем черный цвет значения
                    txt23.SetForegroundColour(wx.BLACK)
                    txt23.Refresh()
                    txt23.SetToolTip(wx.ToolTip(""))               
            else:
                t_month = float(TwoPointThree)
                
                txt23.SetForegroundColour(wx.RED)
                txt23.Refresh()
                # Выводим предупреждающую надпись    
                txt23.SetToolTip(wx.ToolTip("Внимание ошибка! Введено положительное значение температуры"))  
        
#-----------------------------------------------------------------------------------------------------------------
# Проверка четвертого поля    

    def onCheckSecondTabFourthField(self, event):
        
        """ Проверяем четвертое поле. 2.4 Максимальная температура наиболее теплого месяца. """   
        
        # Задаем значения
        TwoPointFour = txt24.GetValue()

        # Делаем проверку на отрицательность
        if TwoPointFour == '':
            txt24.SetToolTip(wx.ToolTip("введите значение"))
        else:
            t_maxh = str(TwoPointFour)
            
            # Проверка на отрицательность значения
            if t_maxh < '0':
                # Если значение вне диапазона
                txt24.SetForegroundColour(wx.RED)
                txt24.Refresh()
                # Выводим предупреждающую надпись    
                txt24.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение температуры"))     
            else:
                t_maxh = float(TwoPointFour)
                
                txt24.SetForegroundColour(wx.BLACK)
                txt24.Refresh()
                txt24.SetToolTip(wx.ToolTip(""))   
                
########################################################################
class TabPanelThree(wx.Panel):
    
    """
    Третья вкладка
    
    """
#----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        # Объявляем глобальные переменные
        global txt31, txt32, txt33, txt34, txt35
        
#---------- Первое поле --------------
        
        # Задаем сайзеры (вертикальный и горизонтальный)
        ThirdSizer_vert = wx.BoxSizer(wx.VERTICAL)
        ThirdSizer_horiz1 = wx.BoxSizer(wx.HORIZONTAL) 
        
        ThirdSizer_vert.AddSpacer(60)
        ThirdSizer_horiz1.AddSpacer(60)
        
        ThirdSizer_vert.Add (ThirdSizer_horiz1)
        
        font31 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text31 = wx.StaticText(self, wx.ID_ANY, "Плотность нефтяного флюида в условиях пласта, кг/м3")
        text31.SetFont(font31)
        text31.SetForegroundColour('black')
        self.Show(True)
        
        # Рисуем поле
        txt31 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        # Обрабатываем событие
        txt31.Bind(wx.EVT_TEXT, self.onCheckThirdTabFirstField)
       
        # Задаем дистанцию между текстом и полем 
        ThirdSizer_horiz1.Add(text31, flag = wx.ALL, border = 10)
        ThirdSizer_horiz1.Add(txt31, flag = wx.ALL, border = 10)
        
#--------- Второе поле ----------                

        ThirdSizer_horiz2 = wx.BoxSizer(wx.HORIZONTAL) 

        ThirdSizer_vert.Add (ThirdSizer_horiz2)
        
        # Добавляем пробелов
        ThirdSizer_horiz2.AddSpacer(80)
    
        font32 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text32 = wx.StaticText(self, wx.ID_ANY, "Вязкость нефтяного флюида, мПа*с")
        text32.SetFont(font32)
        text32.SetForegroundColour('black')
        self.Show(True)
        
        txt32 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt32.Bind(wx.EVT_TEXT, self.onCheckThirdTabSecondField)
        
        # Задаем дистанцию между текстом и полем 
        ThirdSizer_horiz2.Add(text32, flag = wx.ALL, border = 10)
        ThirdSizer_horiz2.Add(txt32, flag = wx.ALL, border = 10)
        
#--------- Третье поле ----------- 

        ThirdSizer_horiz3 = wx.BoxSizer(wx.HORIZONTAL) 

        ThirdSizer_vert.Add (ThirdSizer_horiz3)
        
        # Добавляем пробелов
        ThirdSizer_horiz3.AddSpacer(100)
       
        font33 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text33 = wx.StaticText(self, wx.ID_ANY, "Давление насыщения в условиях пласта, МПа")
        text33.SetFont(font33)
        text33.SetForegroundColour('black')
        self.Show(True)
        
        txt33 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt33.Bind(wx.EVT_TEXT, self.onCheckThirdTabThirdField)
        
        # Задаем дистанцию между текстом и полем 
        ThirdSizer_horiz3.Add(text33, flag = wx.ALL, border = 15)
        ThirdSizer_horiz3.Add(txt33, flag = wx.ALL, border = 15)
        
#--------- Четвертое поле ----------- 

        ThirdSizer_horiz4 = wx.BoxSizer(wx.HORIZONTAL) 

        ThirdSizer_vert.Add (ThirdSizer_horiz4)
        
        # Добавляем пробелов
        ThirdSizer_horiz4.AddSpacer(80)

        font34 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text34 = wx.StaticText(self, wx.ID_ANY, "Температурный коэффициент давления насыщения")
        text34.SetFont(font34)
        text34.SetForegroundColour('black')
        self.Show(True)
        
        txt34 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt34.Bind(wx.EVT_TEXT, self.onCheckThirdTabFourthField)
        
        # Задаем дистанцию между текстом и полем 
        ThirdSizer_horiz4.Add(text34, flag = wx.ALL, border = 15)
        ThirdSizer_horiz4.Add(txt34, flag = wx.ALL, border = 15)
        
#--------- Пятое поле -----------

        ThirdSizer_horiz5 = wx.BoxSizer(wx.HORIZONTAL) 

        ThirdSizer_vert.Add (ThirdSizer_horiz5)
        
        # Добавляем пробелов
        ThirdSizer_horiz5.AddSpacer(100)
        
        font35 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text35 = wx.StaticText(self, wx.ID_ANY, "Газосодержание пластовой жидкости, м3/м3")
        text35.SetFont(font35)
        text35.SetForegroundColour('black')
        self.Show(True)
        
        txt35 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt35.Bind(wx.EVT_TEXT, self.onCheckThirdTabFifthField)
        
        # Задаем дистанцию между текстом и полем 
        ThirdSizer_horiz5.Add(text35, flag = wx.ALL, border = 15)
        ThirdSizer_horiz5.Add(txt35, flag = wx.ALL, border = 15)
        
#-------------------------------------------------------------------------------------------------------
        
        wx.StaticLine(self, pos=(30, 400), size=(950,2))
        
        self.NextThreeTabButton = wx.Button(self, wx.ID_OK, label="следующая>", pos=(500, 700))
        self.NextThreeTabButton.Enable()
        
        self.NextThreeTabButton.Bind(wx.EVT_BUTTON, self.OnCheckThirdTab, self.NextThreeTabButton)
        
        self.CloseThreeTabButton = wx.Button(self, wx.ID_OK, label="Закрыть", pos=(650, 700))
        self.CloseThreeTabButton.Bind(wx.EVT_BUTTON, self.onCloseDataTabThree, self.CloseThreeTabButton)
        
        self.SetSizer(ThirdSizer_vert)
#-----------------------------------------------------------------------------------------------------------------        
# Закрываем окно ноутбука

    def onCloseDataTabThree(self, event):
        """ Закрываем ноутбук с данными """      
  
        self.GetTopLevelParent().Destroy()
#-----------------------------------------------------------------------------------------------------------------

    # Переходим на четвертую вкладку
    def OnCheckThirdTab(self, event):
        
        # Контрольные значения
        ThreePointOne = txt31.GetValue()
        ThreePointTwo = txt32.GetValue()
        ThreePointThree = txt33.GetValue()
        ThreePointFour = txt34.GetValue()
        ThreePointFive = txt35.GetValue()

        
        if ThreePointOne and ThreePointTwo and ThreePointThree and ThreePointFour and ThreePointFive != '':
            
            # Переходим на следующую вкладку
            self.notebook = self.GetParent()
            self.notebook.SetSelection(3)
            
            # Если все поля заполнены - делаем кнопку 'следующая' неактивной
            self.NextThreeTabButton.Enable()
            
             # Делаем вкладку неактивной
#             self.notebook.EnableTab(2, False)
           
        else:
            # Выводим сообщение
            wx.MessageBox(u'Чтобы перейти к следующей вкладке, пожалуйста, заполните все пустые поля', 'Ошибка ввода данных', wx.OK | wx.ICON_ERROR)
            
#-----------------------------------------------------------------------------------------------------------------
# Проверка первого поля    

    def onCheckThirdTabFirstField(self, event):
        
        """ Проверяем первое поле. 3.1 Плотность нефтяного флюида в условиях пласта. """   
        
        # Задаем значения
        ThreePointOne = txt31.GetValue()
        
        # Делаем проверку на отрицательность
        if ThreePointOne == '':
            txt31.SetToolTip(wx.ToolTip("введите значение"))
        else:
            ro = str(ThreePointOne)
            
            # Проверка на отрицательность значения
            if ro < '0':
                # Если значение вне диапазона
                txt31.SetForegroundColour(wx.RED)
                txt31.Refresh()
                # Выводим предупреждающую надпись    
                txt31.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение плотности"))     
            else:
                ro = float(ThreePointOne)
                
                if ro >= 600 and ro <= 950:
                    txt31.SetForegroundColour(wx.BLACK)
                    txt31.Refresh()
                    txt31.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt31.SetForegroundColour(wx.RED)
                    txt31.Refresh()
                    # Выводим предупреждающую надпись    
                    txt31.SetToolTip(wx.ToolTip("Внимание ошибка! Значение плотности вне допустимого диапазона")) 
                
#----------------------------------------------------------------------------------------------------------------

# Проверка второго поля    

    def onCheckThirdTabSecondField(self, event):
        
        """ Проверяем второе поле. 3.2 Вязкость нефтяного флюида в условиях пласта. """   
        
        # Задаем значения
        ThreePointTwo = txt32.GetValue()

        # Делаем проверку на отрицательность
        if ThreePointTwo == '':
            txt32.SetToolTip(wx.ToolTip("введите значение"))
        else:
            visc_plast = str(ThreePointTwo)
            
            # Проверка на отрицательность значения
            if visc_plast < '0':
                # Если значение вне диапазона
                txt32.SetForegroundColour(wx.RED)
                txt32.Refresh()
                # Выводим предупреждающую надпись    
                txt32.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение вязкости"))     
            else:
                visc_plast = float(ThreePointTwo)
                
                if visc_plast >= 1 and visc_plast <= 200:
                    txt32.SetForegroundColour(wx.BLACK)
                    txt32.Refresh()
                    txt32.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt32.SetForegroundColour(wx.RED)
                    txt32.Refresh()
                    # Выводим предупреждающую надпись    
                    txt32.SetToolTip(wx.ToolTip("Внимание ошибка! Значение вязкости вне допустимого диапазона")) 

#-------------------------------------------------------------------------------------------------------------------

# Проверка третьего поля    

    def onCheckThirdTabThirdField(self, event):
        
        """ Проверяем второе поле. 3.3 Давление насыщения в условиях пласта. """   
        
        # Задаем значения
        ThreePointThree = txt33.GetValue()

        # Делаем проверку на отрицательность
        if ThreePointThree == '':
            txt33.SetToolTip(wx.ToolTip("введите значение"))
        else:
            pn_plast = str(ThreePointThree)
            
            # Проверка на отрицательность значения
            if pn_plast < '0':
                # Если значение вне диапазона
                txt33.SetForegroundColour(wx.RED)
                txt33.Refresh()
                # Выводим предупреждающую надпись    
                txt33.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение давления насыщения"))     
            else:
                pn_plast = float(ThreePointThree)
                
                if pn_plast > 0 and pn_plast < 30:
                    txt33.SetForegroundColour(wx.BLACK)
                    txt33.Refresh()
                    txt33.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt33.SetForegroundColour(wx.RED)
                    txt33.Refresh()
                    # Выводим предупреждающую надпись    
                    txt33.SetToolTip(wx.ToolTip("Внимание ошибка! Значение вязкости вне допустимого диапазона")) 
#-------------------------------------------------------------------------------------------------------------------
# Проверка четвертого поля    

    def onCheckThirdTabFourthField(self, event):
        
        """ Проверяем четвертое поле. 3.4 Температурный коэффициент давления насыщения. """   
        
        # Задаем значения
        ThreePointFour = txt34.GetValue()

        # Делаем проверку на отрицательность
        if ThreePointFour == '':
            txt34.SetToolTip(wx.ToolTip("введите значение"))
        else:
            tkpn = str(ThreePointFour)
            
            # Проверка на отрицательность значения
            if tkpn < '0':
                # Если значение вне диапазона
                txt34.SetForegroundColour(wx.RED)
                txt34.Refresh()
                # Выводим предупреждающую надпись    
                txt34.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                tkpn = float(ThreePointFour)
                
                if tkpn > 0 and tkpn <= 0.005:
                    txt34.SetForegroundColour(wx.BLACK)
                    txt34.Refresh()
                    txt34.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt34.SetForegroundColour(wx.RED)
                    txt34.Refresh()
                    # Выводим предупреждающую надпись    
                    txt34.SetToolTip(wx.ToolTip("Внимание ошибка! Значение коэффициента находится вне допустимого диапазона")) 
#--------------------------------------------------------------------------------------------------------------------
# Проверка четвертого поля    

    def onCheckThirdTabFifthField(self, event):
        
        """ Проверяем пятое поле. 3.5 Газосодержание пластовой жидкости. """   
        
        # Задаем значения
        ThreePointFive = txt35.GetValue()

        # Делаем проверку на отрицательность
        if ThreePointFive == '':
            txt35.SetToolTip(wx.ToolTip("введите значение"))
        else:
            g_plast = str(ThreePointFive)
            
            # Проверка на отрицательность значения
            if g_plast < '0':
                # Если значение вне диапазона
                txt35.SetForegroundColour(wx.RED)
                txt35.Refresh()
                # Выводим предупреждающую надпись    
                txt35.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение газосодержания"))     
            else:
                g_plast = float(ThreePointFive)
                
                if g_plast > 0 and g_plast < 200:
                    txt35.SetForegroundColour(wx.BLACK)
                    txt35.Refresh()
                    txt35.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt35.SetForegroundColour(wx.RED)
                    txt35.Refresh()
                    # Выводим предупреждающую надпись    
                    txt35.SetToolTip(wx.ToolTip("Внимание ошибка! Значение газосодержания вне допустимого диапазона")) 
        
########################################################################
class TabPanelFour(wx.Panel):
    
    """
    Четвертая вкладка
    
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        
        """  """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        # Объявляем глобальные переменные
        global txt41, txt42, txt43, txt44, txt45, txt46, txt47, txt48, txt49, txt410
        
#---------- Первое поле --------------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_vert = wx.BoxSizer(wx.VERTICAL)
        FourthSizer_horiz1 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_vert.AddSpacer(40)
        FourthSizer_horiz1.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz1)
        
        font41 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')   
        text41 = wx.StaticText(self, wx.ID_ANY, "Дебит по жидкости (с чистой НКТ), м3/сут")
        text41.SetFont(font41)
        text41.SetForegroundColour('black')
        self.Show(True)
             
        txt41 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt41.Bind(wx.EVT_TEXT, self.onCheckFourthTabFirstField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz1.Add(text41, flag = wx.ALL, border = 15)
        FourthSizer_horiz1.Add(txt41, flag = wx.ALL, border = 15)
        
#---------- Второе поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz2 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz2.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz2)
                
        font42 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text42 = wx.StaticText(self, wx.ID_ANY, "Дебит по нефти, т/сут")
        text42.SetFont(font42)
        text42.SetForegroundColour('black')
        self.Show(True)
        
        txt42 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt42.Bind(wx.EVT_TEXT, self.onCheckFourthTabSecondField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz2.Add(text42, flag = wx.ALL, border = 15)
        FourthSizer_horiz2.Add(txt42, flag = wx.ALL, border = 15)
        
#---------- Третье поле ---------
        
        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz3 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz3.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz3)

        font43 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text43 = wx.StaticText(self, wx.ID_ANY, "Газовый фактор, м3/м3")
        text43.SetFont(font43)
        text43.SetForegroundColour('black')
        self.Show(True)
        
        txt43 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt43.Bind(wx.EVT_TEXT, self.onCheckFourthTabThirdField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz3.Add(text43, flag = wx.ALL, border = 15)
        FourthSizer_horiz3.Add(txt43, flag = wx.ALL, border = 15)
        
#---------- Четвертое поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz4 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz4.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz4)
        
        font44 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text44 = wx.StaticText(self, wx.ID_ANY, "Содержание воды, массовая доля, %")
        text44.SetFont(font44)
        text44.SetForegroundColour('black')
        self.Show(True)

        txt44 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt44.Bind(wx.EVT_TEXT, self.onCheckFourthTabFourthField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz4.Add(text44, flag = wx.ALL, border = 15)
        FourthSizer_horiz4.Add(txt44, flag = wx.ALL, border = 15)
        
#---------- Пятое поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz5 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz5.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz5)
        
        font45 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text45 = wx.StaticText(self, wx.ID_ANY, "Динамический уровень, м")
        text45.SetFont(font45)
        text45.SetForegroundColour('black')
        self.Show(True)
        
        txt45 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt45.Bind(wx.EVT_TEXT, self.onCheckFourthTabFifthField)
        
         # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz5.Add(text45, flag = wx.ALL, border = 15)
        FourthSizer_horiz5.Add(txt45, flag = wx.ALL, border = 15)
        
#---------- Шестое поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz6 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz6.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz6)
        

        font46 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text46 = wx.StaticText(self, wx.ID_ANY, "Давление на устье, МПа")
        text46.SetFont(font46)
        text46.SetForegroundColour('black')
        self.Show(True)
        
        txt46 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt46.Bind(wx.EVT_TEXT, self.onCheckFourthTabSixthField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz6.Add(text46, flag = wx.ALL, border = 15)
        FourthSizer_horiz6.Add(txt46, flag = wx.ALL, border = 15)

#---------- Седьмое поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz7 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz7.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz7)
    
        font47 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text47 = wx.StaticText(self, wx.ID_ANY, "Температура жидкости на выходе из скважины, град. С")
        text47.SetFont(font47)
        text47.SetForegroundColour('black')
        self.Show(True)
        
        txt47 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt47.Bind(wx.EVT_TEXT, self.onCheckFourthTabSeventhField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz7.Add(text47, flag = wx.ALL, border = 15)
        FourthSizer_horiz7.Add(txt47, flag = wx.ALL, border = 15)

#---------- Восьмое поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz8 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz8.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz8)
        
        font48 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text48 = wx.StaticText(self, wx.ID_ANY, "Минимальный дебит по жидкости, м3/сут")
        text48.SetFont(font48)
        text48.SetForegroundColour('black')
        self.Show(True)
        
        txt48 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt48.Bind(wx.EVT_TEXT, self.onCheckFourthTabEighthField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz8.Add(text48, flag = wx.ALL, border = 15)
        FourthSizer_horiz8.Add(txt48, flag = wx.ALL, border = 15)

#---------- Девятое поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz9 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz9.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz9)

        font49 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text49 = wx.StaticText(self, wx.ID_ANY, "Глубина спуска скребка при механической очистке, м")
        text49.SetFont(font48)
        text49.SetForegroundColour('black')
        self.Show(True)
        
        txt49 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt49.Bind(wx.EVT_TEXT, self.onCheckFourthTabNinethField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz9.Add(text49, flag = wx.ALL, border = 15)
        FourthSizer_horiz9.Add(txt49, flag = wx.ALL, border = 15)
        
#---------- Десятое поле ---------

        # Задаем сайзеры (вертикальный и горизонтальный)
        FourthSizer_horiz10 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FourthSizer_horiz10.AddSpacer(40)
        
        FourthSizer_vert.Add (FourthSizer_horiz10)

        font410 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text410 = wx.StaticText(self, wx.ID_ANY, "Максимальная глубина отложения АСПО (по данным КРС), м")
        text410.SetFont(font410)
        text410.SetForegroundColour('black')
        self.Show(True)
       
        txt410 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt410.Bind(wx.EVT_TEXT, self.onCheckFourthTabTenthField)
        
        # Задаем дистанцию между текстом и полем 
        FourthSizer_horiz10.Add(text410, flag = wx.ALL, border = 15)
        FourthSizer_horiz10.Add(txt410, flag = wx.ALL, border = 15)
#------------------------------------------------------------------------------

        wx.StaticLine(self, pos=(30, 650), size=(950,2))
        
        self.NextFourTabButton = wx.Button(self, wx.ID_OK, label="следующая>", pos=(500, 700))
        self.NextFourTabButton.Enable()
        
        self.NextFourTabButton.Bind(wx.EVT_BUTTON, self.OnCheckFourthTab, self.NextFourTabButton)
        
        self.CloseFourTabButton = wx.Button(self, wx.ID_OK, label="Закрыть", pos=(650, 700))
        self.CloseFourTabButton.Bind(wx.EVT_BUTTON, self.onCloseDataTabFour, self.CloseFourTabButton)
        
        self.SetSizer(FourthSizer_vert)

#-----------------------------------------------------------------------------------------------------------------        
# Закрываем окно ноутбука

    def onCloseDataTabFour(self, event):
        """ Закрываем ноутбук с данными """      
  
        self.GetTopLevelParent().Destroy()
    
#-----------------------------------------------------------------------------------------------------------------    

# Переходим на пятую вкладку
    def OnCheckFourthTab(self, event):
        
        # Контрольные значения
        FourPointOne = txt41.GetValue()
        FourPointTwo  = txt42.GetValue()
        FourPointThree = txt43.GetValue()
        FourPointFour = txt44.GetValue()
        FourPointFive = txt45.GetValue()
        FourPointSix = txt46.GetValue()
        FourPointSeven = txt47.GetValue()
        FourPointEight = txt48.GetValue()
        FourPointNine = txt49.GetValue()
        FourPointTen = txt410.GetValue()
        
        if FourPointOne and FourPointTwo and FourPointThree and FourPointFour and FourPointFive and FourPointSix and FourPointSeven and FourPointEight and FourPointNine and FourPointTen != '':
            
            # Переходим на следующую вкладку
            self.notebook = self.GetParent()
            self.notebook.SetSelection(4)
            
            # Если все поля заполнены - делаем кнопку 'следующая' неактивной
            self.NextFourTabButton.Enable()
            
             # Делаем вкладку неактивной
#             self.notebook.EnableTab(3, False)
        else:
            # Выводим сообщение
            wx.MessageBox(u'Чтобы перейти к следующей вкладке, пожалуйста, заполните все пустые поля', 'Ошибка ввода данных', wx.OK | wx.ICON_ERROR)
            
#-----------------------------------------------------------------------------------------------------------------

# Проверка первого поля

    def onCheckFourthTabFirstField(self, event):
        
        """ Проверяем первое поле. 4.1 Дебит по жидкости (с чистой НКТ). """   
        
        # Задаем значения
        FourPointOne = txt41.GetValue()

        # Делаем проверку на отрицательность
        if FourPointOne == '':
            txt41.SetToolTip(wx.ToolTip("введите значение"))
        else:
            nomdebit = str(FourPointOne)
            
            # Проверка на отрицательность значения
            if nomdebit < '0':
                # Если значение вне диапазона
                txt41.SetForegroundColour(wx.RED)
                txt41.Refresh()
                # Выводим предупреждающую надпись    
                txt41.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение дебита"))     
            else:
                nomdebit = float(FourPointOne)
                
                if nomdebit > 0:
                    txt41.SetForegroundColour(wx.BLACK)
                    txt41.Refresh()
                    txt41.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt41.SetForegroundColour(wx.RED)
                    txt41.Refresh()
                    # Выводим предупреждающую надпись    
                    txt41.SetToolTip(wx.ToolTip("Внимание ошибка! Значение дебита вне допустимого диапазона")) 

#-----------------------------------------------------------------------------------------------------------------

# Проверка второго поля

    def onCheckFourthTabSecondField(self, event):
        
        """ Проверяем второе поле. 4.2 Дебит по нефти. """   
        
        # Задаем значения
        FourPointTwo = txt42.GetValue() # дебит по нефти
        FourPointOne = txt41.GetValue() # дебит по жидкости

        # Делаем проверку на отрицательность
        if FourPointTwo == '':
            txt42.SetToolTip(wx.ToolTip("введите значение"))
        else:
            debit_oil = str(FourPointTwo)
            
            # Проверка на отрицательность значения
            if debit_oil < '0':
                # Если значение вне диапазона
                txt42.SetForegroundColour(wx.RED)
                txt42.Refresh()
                # Выводим предупреждающую надпись    
                txt42.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение дебита"))     
            else:
                debit_oil = float(FourPointTwo)
                nomdebit = float(FourPointOne)
                
                if debit_oil > 0 and debit_oil <= nomdebit:
                    txt42.SetForegroundColour(wx.BLACK)
                    txt42.Refresh()
                    txt42.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt42.SetForegroundColour(wx.RED)
                    txt42.Refresh()
                    # Выводим предупреждающую надпись    
                    txt42.SetToolTip(wx.ToolTip("Внимание ошибка! Значение дебита вне допустимого диапазона")) 
#-----------------------------------------------------------------------------------------------------------------

# Проверка третьего поля

    def onCheckFourthTabThirdField(self, event):
        
        """ Проверяем третье поле. 4.3 Газовый фактор. """
            
        
        # Задаем значения
        FourPointThree = txt43.GetValue() # газовый фактор
        ThreePointFive = txt35.GetValue() # газосодержание пластовой нефти

        # Делаем проверку на отрицательность
        if FourPointThree == '':
            txt43.SetToolTip(wx.ToolTip("введите значение"))
        else:
            g = str(FourPointThree)
            
            # Проверка на отрицательность значения
            if g < '0':
                # Если значение вне диапазона
                txt43.SetForegroundColour(wx.RED)
                txt43.Refresh()
                # Выводим предупреждающую надпись    
                txt43.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение газового фактора"))     
            else:
                g = float(FourPointThree)
                g_plast = float(ThreePointFive)
                
                if g > 0 and g <= g_plast:
                    txt43.SetForegroundColour(wx.BLACK)
                    txt43.Refresh()
                    txt43.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt43.SetForegroundColour(wx.RED)
                    txt43.Refresh()
                    # Выводим предупреждающую надпись    
                    txt43.SetToolTip(wx.ToolTip("Внимание ошибка! Значение газового фактора вне допустимого диапазона")) 
                    
#-----------------------------------------------------------------------------------------------------------------

# Проверка четвертого поля

    def onCheckFourthTabFourthField(self, event):
        
        """ Проверяем четвертое поле. 4.4 Содержание воды, массовая доля. """
       
        # Задаем значения
        FourPointFour = txt44.GetValue() 

        # Делаем проверку на отрицательность
        if FourPointFour == '':
            txt44.SetToolTip(wx.ToolTip("введите значение"))
        else:
            water = str(FourPointFour)
            
            # Проверка на отрицательность значения
            if water < '0':
                # Если значение вне диапазона
                txt44.SetForegroundColour(wx.RED)
                txt44.Refresh()
                # Выводим предупреждающую надпись    
                txt44.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение обводненности"))     
            else:
                water = float(FourPointFour)
                              
                if water > 0 and water < 80:
                    txt44.SetForegroundColour(wx.BLACK)
                    txt44.Refresh()
                    txt44.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt44.SetForegroundColour(wx.RED)
                    txt44.Refresh()
                    # Выводим предупреждающую надпись    
                    txt44.SetToolTip(wx.ToolTip("Внимание ошибка! Значение обводненности вне допустимого диапазона")) 
                    
#--------------------------------------------------------------------------------------------------------------------------

# Проверка пятого поля

    def onCheckFourthTabFifthField(self, event):
        
        """ Проверяем пятое поле. 4.5 Динамический уровень. """
       
        # Задаем значения
        FourPointFive = txt45.GetValue() # динамический уровень
        OnePoinSeven = txt17.GetValue()  # длина колонны НКТ 
        OnePoinNine  = txt19.GetValue()  # статический уровень флюида в скважине 

        # Делаем проверку на отрицательность
        if FourPointFive == '':
            txt45.SetToolTip(wx.ToolTip("введите значение"))
        else:
            h_din = str(FourPointFive)
            
            # Проверка на отрицательность значения
            if h_din < '0':
                # Если значение вне диапазона
                txt45.SetForegroundColour(wx.RED)
                txt45.Refresh()
                # Выводим предупреждающую надпись    
                txt45.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение обводненности"))     
            else:
                h_din = float(FourPointFive)
                h_nkt = float(OnePoinSeven)
                h_stat = float(OnePoinNine)
                              
                if h_din > h_stat and h_din < h_nkt:
                    txt45.SetForegroundColour(wx.BLACK)
                    txt45.Refresh()
                    txt45.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt45.SetForegroundColour(wx.RED)
                    txt45.Refresh()
                    # Выводим предупреждающую надпись    
                    txt45.SetToolTip(wx.ToolTip("Внимание ошибка! Значение обводненности вне допустимого диапазона")) 
#-----------------------------------------------------------------------------------------------------------------

# Проверка шестого поля

    def onCheckFourthTabSixthField(self, event):
        
        """" Проверяем шестое поле. 4.6 Давление на устье. """
        
        # Задаем значения
        FourPointSix = txt46.GetValue() 

        # Делаем проверку на отрицательность
        if FourPointSix == '':
            txt46.SetToolTip(wx.ToolTip("введите значение"))
        else:
            p_wellhead = str(FourPointSix)
            
            # Проверка на отрицательность значения
            if p_wellhead < '0':
                # Если значение вне диапазона
                txt46.SetForegroundColour(wx.RED)
                txt46.Refresh()
                # Выводим предупреждающую надпись    
                txt46.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение давления"))     
            else:
                p_wellhead = float(FourPointSix)
                              
                if p_wellhead > 1:
                    txt46.SetForegroundColour(wx.BLACK)
                    txt46.Refresh()
                    txt46.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt46.SetForegroundColour(wx.RED)
                    txt46.Refresh()
                    # Выводим предупреждающую надпись    
                    txt46.SetToolTip(wx.ToolTip("Внимание ошибка! Значение давления вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка седьмого поля

    def onCheckFourthTabSeventhField(self, event):
        
        """" Проверяем седьмое поле. 4.7 Температура жидкости на выходе из скважины. """
           
        # Задаем значения
        FourPointSeven = txt47.GetValue() # температура жидкости на выходе из скважины
        TwoPointOne = txt21.GetValue()    # температура нефтяного пласта

        # Делаем проверку на отрицательность
        if FourPointSeven == '':
            txt47.SetToolTip(wx.ToolTip("введите значение"))
        else:
            t_wellhead = str(FourPointSeven)
            # Проверка на отрицательность значения
            if t_wellhead < '0':
                # Если значение вне диапазона
                txt47.SetForegroundColour(wx.RED)
                txt47.Refresh()
                # Выводим предупреждающую надпись    
                txt47.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение давления"))     
            else:
                t_wellhead = float(FourPointSeven)
                t_bhole = float(TwoPointOne)
                              
                if t_wellhead < t_bhole:
                    txt47.SetForegroundColour(wx.BLACK)
                    txt47.Refresh()
                    txt47.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt47.SetForegroundColour(wx.RED)
                    txt47.Refresh()
                    # Выводим предупреждающую надпись    
                    txt47.SetToolTip(wx.ToolTip("Внимание ошибка! Значение давления вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка восьмого поля

    def onCheckFourthTabEighthField(self, event):
        
        """" Проверяем восьмое поле. 4.8 Минимальный дебит по жидкости. """
        
        # Задаем значения
        FourPointEight = txt48.GetValue() # минимальный дебит по жидкости
        FourPointOne = txt41.GetValue()   # дебит по жидкости (с чистой НКТ)

        # Делаем проверку на отрицательность
        if FourPointEight == '':
            txt48.SetToolTip(wx.ToolTip("введите значение"))
        else:
            debit = str(FourPointEight)
            # Проверка на отрицательность значения
            if debit < '0':
                # Если значение вне диапазона
                txt48.SetForegroundColour(wx.RED)
                txt48.Refresh()
                # Выводим предупреждающую надпись    
                txt48.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение дебита"))     
            else:
                debit = float(FourPointEight)
                nomdebit = float(FourPointOne)
                              
                if debit <= nomdebit:
                    txt48.SetForegroundColour(wx.BLACK)
                    txt48.Refresh()
                    txt48.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt48.SetForegroundColour(wx.RED)
                    txt48.Refresh()
                    # Выводим предупреждающую надпись    
                    txt48.SetToolTip(wx.ToolTip("Внимание ошибка! Значение дебита вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка девятого поля

    def onCheckFourthTabNinethField(self, event):
        
        """" Проверяем девятое поле. 4.9 Глубина спуска скребка при механической очистке. """
 
        # Задаем значения
        FourPointNine = txt49.GetValue() # глубина спуска скребка при механической очистке
        OnePoinSeven = txt17.GetValue()  # длина колонны НКТ 

        # Делаем проверку на отрицательность
        if FourPointNine == '':
            txt49.SetToolTip(wx.ToolTip("введите значение"))
        else:
            scraper = str(FourPointNine)
            # Проверка на отрицательность значения
            if scraper < '0':
                # Если значение вне диапазона
                txt49.SetForegroundColour(wx.RED)
                txt49.Refresh()
                # Выводим предупреждающую надпись    
                txt49.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение глубины"))     
            else:
                scraper = float(FourPointNine)
                h_nkt = float(OnePoinSeven)
                              
                if scraper < h_nkt:
                    txt49.SetForegroundColour(wx.BLACK)
                    txt49.Refresh()
                    txt49.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt49.SetForegroundColour(wx.RED)
                    txt49.Refresh()
                    # Выводим предупреждающую надпись    
                    txt49.SetToolTip(wx.ToolTip("Внимание ошибка! Значение глубины вне допустимого диапазона"))

#-----------------------------------------------------------------------------------------------------------------

# Проверка десятого поля

    def onCheckFourthTabTenthField(self, event):
    
        """" Проверяем десятое поле. 4.10 Максимальная глубина отложения АСПО. """
 
        # Задаем значения
        FourPointTen = txt410.GetValue() # максимальная глубина отложения АСПО
        OnePoinSeven = txt17.GetValue()  # длина колонны НКТ 

        # Делаем проверку на отрицательность
        if FourPointTen == '':
            txt410.SetToolTip(wx.ToolTip("введите значение"))
        else:
            h_aspo = str(FourPointTen)
            # Проверка на отрицательность значения
            if h_aspo < '0':
                # Если значение вне диапазона
                txt410.SetForegroundColour(wx.RED)
                txt410.Refresh()
                # Выводим предупреждающую надпись    
                txt410.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение глубины"))     
            else:
                h_aspo = float(FourPointTen)
                h_nkt = float(OnePoinSeven)
                              
                if h_aspo < h_nkt:
                    txt410.SetForegroundColour(wx.BLACK)
                    txt410.Refresh()
                    txt410.SetToolTip(wx.ToolTip(""))   
                else:
                    # Если значение вне диапазона
                    txt410.SetForegroundColour(wx.RED)
                    txt410.Refresh()
                    # Выводим предупреждающую надпись    
                    txt410.SetToolTip(wx.ToolTip("Внимание ошибка! Значение глубины вне допустимого диапазона"))
                    
########################################################################
class TabPanelFive(wx.Panel):
    
    """
    Пятая вкладка
    
    """
#----------------------------------------------------------------------
    def __init__(self, parent):
        """ """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        # Объявляем глобальные переменные
        global txt51, txt52, txt53, txt54, txt55, txt56, txt57, txt58, txt59, txt510
        
#------ Первое поле ----------

        FifthSizer_vert = wx.BoxSizer(wx.VERTICAL) 
        FifthSizer_horiz1 = wx.BoxSizer(wx.HORIZONTAL) 
        
        FifthSizer_vert.AddSpacer(40)
        FifthSizer_horiz1.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz1)

        font51 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text51 = wx.StaticText(self, wx.ID_ANY, "Плотность дегазированной нефти в норм. условиях, кг/м3")
        text51.SetFont(font51)
        text51.SetForegroundColour('black')
        self.Show(True)
        
        txt51 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt51.Bind(wx.EVT_TEXT, self.onCheckFiveTabFirstField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz1.Add(text51, flag = wx.ALL, border = 15)
        FifthSizer_horiz1.Add(txt51, flag = wx.ALL, border = 15)
        
#------ Второе поле ----------

        FifthSizer_horiz2 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz2.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz2)
    
        font52 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text52 = wx.StaticText(self, wx.ID_ANY, "Вязкость дегазированной нефти, мПа*с")
        text52.SetFont(font52)
        text52.SetForegroundColour('black')
        self.Show(True)
        
        txt52 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt52.Bind(wx.EVT_TEXT, self.onCheckFiveTabSecondField)
        
         # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz2.Add(text52, flag = wx.ALL, border = 15)
        FifthSizer_horiz2.Add(txt52, flag = wx.ALL, border = 15) 
        
#------ Третье поле ----------

        FifthSizer_horiz3 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz3.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz3)

        font53 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text53 = wx.StaticText(self, wx.ID_ANY, "Содержание парафина, массовая доля, %")
        text53.SetFont(font53)
        text53.SetForegroundColour('black')
        self.Show(True)
        
        txt53 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt53.Bind(wx.EVT_TEXT, self.onCheckFiveTabThirdField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz3.Add(text53, flag = wx.ALL, border = 15)
        FifthSizer_horiz3.Add(txt53, flag = wx.ALL, border = 15)
        
#------ Четвертое поле ----------

        FifthSizer_horiz4 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz4.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz4)
        
        font54 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text54 = wx.StaticText(self, wx.ID_ANY, "Содержание асфальтенов, массовая доля, %")
        text54.SetFont(font54)
        text54.SetForegroundColour('black')
        self.Show(True)
        
        txt54 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt54.Bind(wx.EVT_TEXT, self.onCheckFiveTabFourthField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz4.Add(text54, flag = wx.ALL, border = 15)
        FifthSizer_horiz4.Add(txt54, flag = wx.ALL, border = 15)
        
#------ Пятое поле ----------

        FifthSizer_horiz5 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz5.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz5)
        
        font55 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text55 = wx.StaticText(self, wx.ID_ANY, "Содержание смол селикогелевых, массовая доля, %")
        text55.SetFont(font55)
        text55.SetForegroundColour('black')
        self.Show(True)
        
        txt55 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt55.Bind(wx.EVT_TEXT, self.onCheckFiveTabFifthField)
        
         # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz5.Add(text55, flag = wx.ALL, border = 15)
        FifthSizer_horiz5.Add(txt55, flag = wx.ALL, border = 15)
                
#------ Шестое поле ----------

        FifthSizer_horiz6 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz6.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz6)
        
        font56 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text56 = wx.StaticText(self, wx.ID_ANY, "Температура застывания нефти, град. С")
        text56.SetFont(font56)
        text56.SetForegroundColour('black')
        self.Show(True)
        
        txt56 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt56.Bind(wx.EVT_TEXT, self.onCheckFiveTabSixthField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz6.Add(text56, flag = wx.ALL, border = 15)
        FifthSizer_horiz6.Add(txt56, flag = wx.ALL, border = 15)
                
#------ Седьмое поле ----------
        
        FifthSizer_horiz7 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz7.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz7)
        
        font57 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text57 = wx.StaticText(self, wx.ID_ANY, "Температура насыщения нефти парафином, град. С")
        text57.SetFont(font57)
        text57.SetForegroundColour('black')
        self.Show(True)
        
        txt57 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt57.Bind(wx.EVT_TEXT, self.onCheckFiveTabSeventhField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz7.Add(text57, flag = wx.ALL, border = 15)
        FifthSizer_horiz7.Add(txt57, flag = wx.ALL, border = 15)
        
#------ Восьмое поле ----------

        FifthSizer_horiz8 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz8.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz8)
        
        font58 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text58 = wx.StaticText(self, wx.ID_ANY, "Температура плавления парафинов, град. С")
        text58.SetFont(font58)
        text58.SetForegroundColour('black')
        self.Show(True)
        
        txt58 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt58.Bind(wx.EVT_TEXT, self.onCheckFiveTabEighthField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz8.Add(text58, flag = wx.ALL, border = 15)
        FifthSizer_horiz8.Add(txt58, flag = wx.ALL, border = 15)
                
#------ Девятое поле ----------

        FifthSizer_horiz9 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz9.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz9)
        
        font59 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text59 = wx.StaticText(self, wx.ID_ANY, "Плотность сопутствующего газа, кг/м3")
        text59.SetFont(font58)
        text59.SetForegroundColour('black')
        self.Show(True)
        
        txt59 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt59.Bind(wx.EVT_TEXT, self.onCheckFiveTabNinthField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz9.Add(text59, flag = wx.ALL, border = 15)
        FifthSizer_horiz9.Add(txt59, flag = wx.ALL, border = 15)
                
#------ Десятое поле ----------

        FifthSizer_horiz10 = wx.BoxSizer(wx.HORIZONTAL)
    
        FifthSizer_horiz10.AddSpacer(40)
        
        FifthSizer_vert.Add (FifthSizer_horiz10)
            
        font510 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text510 = wx.StaticText(self, wx.ID_ANY, "Плотность сопутствующей воды, кг/м3")
        text510.SetFont(font510)
        text510.SetForegroundColour('black')
        self.Show(True)
        
        txt510 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt510.Bind(wx.EVT_TEXT, self.onCheckFiveTabTenthField)
        
        # Задаем дистанцию между текстом и полем 
        FifthSizer_horiz10.Add(text510, flag = wx.ALL, border = 15)
        FifthSizer_horiz10.Add(txt510, flag = wx.ALL, border = 15)
        
#------------------------------------------------------------------------------------------------        
      
        wx.StaticLine(self, pos=(30, 650), size=(950,2))
        
        self.NextFiveTabButton = wx.Button(self, wx.ID_OK, label="следующая>", pos=(500, 700))
        
#         self.CloseFiveTabButton.Enable()
        
        self.Bind(wx.EVT_BUTTON, self.OnCheckFifthTab, self.NextFiveTabButton)
        
        self.CloseFiveTabButton = wx.Button(self, wx.ID_OK, label="Закрыть", pos=(650, 700))
        
        self.CloseFiveTabButton.Bind(wx.EVT_BUTTON, self.onCloseDataTabFive, self.CloseFiveTabButton)
        
        self.SetSizer(FifthSizer_vert)
#-----------------------------------------------------------------------------------------------------------------        
# Закрываем окно ноутбука

    def onCloseDataTabFive(self, event):
        """ Закрываем ноутбук с данными """      
  
        self.GetTopLevelParent().Destroy()
#----------------------------------------------------------------------------------------------------------------

# Переходим на шестую вкладку
    def OnCheckFifthTab(self, event):
        
        # Контрольные значения
        FivePointOne = txt51.GetValue()
        FivePointTwo = txt52.GetValue()
        FivePointThree = txt53.GetValue()
        FivePointFour = txt54.GetValue()
        FivePointFive = txt55.GetValue()
        FivePointSix = txt56.GetValue()
        FivePointSeven = txt57.GetValue()
        FivePointEight = txt58.GetValue()
        FivePointNine = txt59.GetValue()
        FivePointTen = txt510.GetValue()

        if FivePointOne and FivePointTwo and FivePointThree and FivePointFour and FivePointFive and FivePointSix and FivePointSeven and FivePointEight and FivePointNine and FivePointTen != '':
            
            # Переходим на следующую вкладку
            self.notebook = self.GetParent()
            self.notebook.SetSelection(5)
            
            # Если все поля заполнены - делаем кнопку 'следующая' неактивной
            self.NextFiveTabButton.Enable()
            
             # Делаем вкладку неактивной
#             self.notebook.EnableTab(4, False)
           
        else:
            # Выводим сообщение
            wx.MessageBox(u'Чтобы перейти к следующей вкладке, пожалуйста, заполните все пустые поля', 'Ошибка ввода данных', wx.OK | wx.ICON_ERROR)
#-----------------------------------------------------------------------------------------------------------------

# Проверка первого поля

    def onCheckFiveTabFirstField(self, event):
        
        """ Проверяем первое поле. 5.1 Плотность дегазированной нефти в нормальных условиях. """ 
        
        # Задаем значения
        FivePointOne = txt51.GetValue() # плотность дегазированной нефти в нормальных условиях
        ThreePoinOne = txt31.GetValue() # плотность нефтяного флюида в условиях пласта

        # Делаем проверку 
        if FivePointOne == '':
            txt51.SetToolTip(wx.ToolTip("введите значение"))
        else:
            ro_oil = str(FivePointOne)
            # Проверка на отрицательность значения
            if ro_oil < '0':
                # Если значение вне диапазона
                txt51.SetForegroundColour(wx.RED)
                txt51.Refresh()
                # Выводим предупреждающую надпись    
                txt51.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение плотности"))     
            else:
                ro_oil = float(FivePointOne)
                ro = float(ThreePoinOne)
                              
                if ro_oil >= 700 and ro_oil <= 1020 and ro_oil > ro:
                    
                    txt51.SetForegroundColour(wx.BLACK)
                    txt51.Refresh()
                    txt51.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt51.SetForegroundColour(wx.RED)
                    txt51.Refresh()
                    # Выводим предупреждающую надпись    
                    txt51.SetToolTip(wx.ToolTip("Внимание ошибка! Значение плотности вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка второго поля

    def onCheckFiveTabSecondField(self, event):
        
        """ Проверяем второе поле. 5.2 Вязкость дегазированной нефти. """ 
        
        # Задаем значения
        FivePointTwo = txt52.GetValue() # вязкость дегазированной нефти
        ThreePoinTwo = txt32.GetValue() # вязкость нефтяного флюида

        # Делаем проверку
        if FivePointTwo == '':
            txt52.SetToolTip(wx.ToolTip("введите значение"))
        else:
            visc_oil = str(FivePointTwo)
            # Проверка на отрицательность значения
            if visc_oil < '0':
                # Если значение вне диапазона
                txt52.SetForegroundColour(wx.RED)
                txt52.Refresh()
                # Выводим предупреждающую надпись    
                txt52.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение вязкости"))     
            else:
                visc_oil = float(FivePointTwo)
                visc_plast = float(ThreePoinTwo)
                              
                if visc_oil > 1 and visc_oil > visc_plast:
                    
                    txt52.SetForegroundColour(wx.BLACK)
                    txt52.Refresh()
                    txt52.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt52.SetForegroundColour(wx.RED)
                    txt52.Refresh()
                    # Выводим предупреждающую надпись    
                    txt52.SetToolTip(wx.ToolTip("Внимание ошибка! Значение вязкости вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка третьего поля

    def onCheckFiveTabThirdField(self, event):
        
        """ Проверяем третье поле. 5.3 Содержание парафина, массовая доля. """ 
        
        # Задаем значения
        FivePointThree = txt53.GetValue() # cодержание парафина, массовая доля
    
        # Делаем проверку 
        if FivePointThree == '':
            txt53.SetToolTip(wx.ToolTip("введите значение"))
        else:
            cp = str(FivePointThree)
            # Проверка на отрицательность значения
            if cp < '0':
                # Если значение вне диапазона
                txt53.SetForegroundColour(wx.RED)
                txt53.Refresh()
                # Выводим предупреждающую надпись    
                txt53.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение концентрации парафина"))     
            else:
                cp = float(FivePointThree)
                             
                if cp >= 0 and cp < 25:
                    txt53.SetForegroundColour(wx.BLACK)
                    txt53.Refresh()
                    txt53.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt53.SetForegroundColour(wx.RED)
                    txt53.Refresh()
                    # Выводим предупреждающую надпись    
                    txt53.SetToolTip(wx.ToolTip("Внимание ошибка! Слишком много парафинов"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка четвертого поля

    def onCheckFiveTabFourthField(self, event):
        
        """ Проверяем четвертое поле. 5.4 Содержание асфальтенов, массовая доля. """ 
        
        # Задаем значения
        FivePointFour = txt54.GetValue() # cодержание асфальтенов, массовая доля
    
        # Делаем проверку 
        if FivePointFour == '':
            txt54.SetToolTip(wx.ToolTip("введите значение"))
        else:
            asf = str(FivePointFour)
            # Проверка на отрицательность значения
            if asf < '0':
                # Если значение вне диапазона
                txt54.SetForegroundColour(wx.RED)
                txt54.Refresh()
                # Выводим предупреждающую надпись    
                txt54.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение концентрации асфальтенов"))     
            else:
                asf = float(FivePointFour)
                             
                if asf >= 0 and asf <= 30:
                    txt54.SetForegroundColour(wx.BLACK)
                    txt54.Refresh()
                    txt54.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt54.SetForegroundColour(wx.RED)
                    txt54.Refresh()
                    # Выводим предупреждающую надпись    
                    txt54.SetToolTip(wx.ToolTip("Внимание ошибка! Значение концентрации асфальтенов вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка пятого поля

    def onCheckFiveTabFifthField(self, event):
        
        """ Проверяем пятое поле. 5.5 Содержание силикагелевых смол, массовая доля. """ 
        
        # Задаем значения
        FivePointFive = txt55.GetValue() # cодержание силикагелевых смол, массовая доля
    
        # Делаем проверку 
        if FivePointFive == '':
            txt55.SetToolTip(wx.ToolTip("введите значение"))
        else:
            silica_gel = str(FivePointFive)
            # Проверка на отрицательность значения
            if silica_gel < '0':
                # Если значение вне диапазона
                txt55.SetForegroundColour(wx.RED)
                txt55.Refresh()
                # Выводим предупреждающую надпись    
                txt55.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение концентрации смол"))     
            else:
                silica_gel = float(FivePointFive)
                             
                if silica_gel >= 0 and silica_gel <= 30:
                    txt55.SetForegroundColour(wx.BLACK)
                    txt55.Refresh()
                    txt55.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt55.SetForegroundColour(wx.RED)
                    txt55.Refresh()
                    # Выводим предупреждающую надпись    
                    txt55.SetToolTip(wx.ToolTip("Внимание ошибка! Значение концентрации смол вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка шестого поля

    def onCheckFiveTabSixthField(self, event):
        
        """ Проверяем шестое поле. 5.6 Температура застывания нефти. """ 
        
        # Задаем значения
        FivePointSix = txt56.GetValue() # температура застывания нефти
    
        # Делаем проверку 
        if FivePointSix == '':
            txt56.SetToolTip(wx.ToolTip("введите значение"))
        else:
            freezing_oil = str(FivePointSix)
            # Проверка на отрицательность значения
            if freezing_oil < '0':
                # Если значение вне диапазона
                txt56.SetForegroundColour(wx.RED)
                txt56.Refresh()
                # Выводим предупреждающую надпись    
                txt56.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение температуры"))     
            else:
                freezing_oil = float(FivePointSix)
                             
                if freezing_oil != 0 and freezing_oil <= 60:
                    txt56.SetForegroundColour(wx.BLACK)
                    txt56.Refresh()
                    txt56.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt56.SetForegroundColour(wx.RED)
                    txt56.Refresh()
                    # Выводим предупреждающую надпись    
                    txt56.SetToolTip(wx.ToolTip("Внимание ошибка! Значение температуры вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка седьмого поля
    
    def onCheckFiveTabSeventhField(self, event):
        
        """ Проверяем седьмое поле. 5.7 Температура насыщения нефти парафином. """ 
        
        # Задаем значения
        FivePointSeven = txt57.GetValue() # температура насыщения нефти парафином
        FivePointSix = txt56.GetValue() # температура застывания нефти
    
        # Делаем проверку 
        if FivePointSeven == '':
            txt57.SetToolTip(wx.ToolTip("введите значение"))
        else:
            t_0 = str(FivePointSeven)
            # Проверка на отрицательность значения
            if t_0 < '0':
                # Если значение вне диапазона
                txt57.SetForegroundColour(wx.RED)
                txt57.Refresh()
                # Выводим предупреждающую надпись    
                txt57.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение температуры"))     
            else:
                t_0 = float(FivePointSeven)
                freezing_oil = float(FivePointSix)
                             
                if t_0 != 0 and t_0 != freezing_oil and t_0 <= 60:
                    txt57.SetForegroundColour(wx.BLACK)
                    txt57.Refresh()
                    txt57.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt57.SetForegroundColour(wx.RED)
                    txt57.Refresh()
                    # Выводим предупреждающую надпись    
                    txt57.SetToolTip(wx.ToolTip("Внимание ошибка! Значение температуры равно нулю"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка восьмого поля

    def onCheckFiveTabEighthField(self, event):
        
        """ Проверяем шестое поле. 5.8 Температура плавления парафинов. """ 
        
        # Задаем значения
        FivePointEight= txt58.GetValue() # температура плавления парафинов 
        FivePointSeven = txt57.GetValue() # температура насыщения нефти парафином
        FivePointSix = txt56.GetValue() # температура застывания нефти
    
        # Делаем проверку 
        if FivePointEight == '':
            txt58.SetToolTip(wx.ToolTip("введите значение"))
        else:
            melting = str(FivePointEight)
            # Проверка на отрицательность значения
            if melting < '0':
                # Если значение вне диапазона
                txt58.SetForegroundColour(wx.RED)
                txt58.Refresh()
                # Выводим предупреждающую надпись    
                txt58.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение температуры"))     
            else:
                melting = float(FivePointEight)
                t_0 = float(FivePointSeven)
                freezing_oil = float(FivePointSix)
                             
                if melting > t_0 and melting > freezing_oil:
                    txt58.SetForegroundColour(wx.BLACK)
                    txt58.Refresh()
                    txt58.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt58.SetForegroundColour(wx.RED)
                    txt58.Refresh()
                    # Выводим предупреждающую надпись    
                    txt58.SetToolTip(wx.ToolTip("Внимание ошибка! Значение температуры вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка девятого поля

    def onCheckFiveTabNinthField(self, event):
        
        """ Проверяем девятое поле. 5.9 Плотность сопутствующего газа. """ 
        
        # Задаем значения
        FivePointNine = txt59.GetValue() # плотность сопутствующего газа
    
        # Делаем проверку 
        if FivePointNine == '':
            txt59.SetToolTip(wx.ToolTip("введите значение"))
        else:
            ro_gas = str(FivePointNine)
            # Проверка на отрицательность значения
            if ro_gas < '0':
                # Если значение вне диапазона
                txt59.SetForegroundColour(wx.RED)
                txt59.Refresh()
                # Выводим предупреждающую надпись    
                txt59.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение плотности"))     
            else:
                ro_gas = float(FivePointNine)
                             
                if ro_gas > 0.65 and ro_gas < 1.3:
                    txt59.SetForegroundColour(wx.BLACK)
                    txt59.Refresh()
                    txt59.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt59.SetForegroundColour(wx.RED)
                    txt59.Refresh()
                    # Выводим предупреждающую надпись    
                    txt59.SetToolTip(wx.ToolTip("Внимание ошибка! Значение плотности вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка десятого поля

    def onCheckFiveTabTenthField(self, event):
        
        """ Проверяем десятое поле. 5.10 Плотность сопутствующей воды. """ 
        
        # Задаем значения
        FivePointTen = txt510.GetValue() # плотность сопутствующей воды
    
        # Делаем проверку 
        if FivePointTen == '':
            txt510.SetToolTip(wx.ToolTip("введите значение"))
        else:
            ro_water = str(FivePointTen)
            # Проверка на отрицательность значения
            if ro_water < '0':
                # Если значение вне диапазона
                txt510.SetForegroundColour(wx.RED)
                txt510.Refresh()
                # Выводим предупреждающую надпись    
                txt510.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение плотности"))     
            else:
                ro_water = float(FivePointTen)
                             
                if ro_water >= 1000 and ro_water <= 1300:
                    txt510.SetForegroundColour(wx.BLACK)
                    txt510.Refresh()
                    txt510.SetToolTip(wx.ToolTip(""))         
                else:
                    # Если значение вне диапазона
                    txt510.SetForegroundColour(wx.RED)
                    txt510.Refresh()
                    # Выводим предупреждающую надпись    
                    txt510.SetToolTip(wx.ToolTip("Внимание ошибка! Значение плотности вне допустимого диапазона"))
                    
#######################################################################
class TabPanelSix(wx.Panel):
    """
    Шестая вкладка
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        # Объявляем глобальные переменные
        global SixTabSaveButton, txt14, txt61, txt65, txt66, txt67, txt68, txt69, txt610, txt611, txt612, txt613, txt614, txt615, txt616
        
#------ Первое поле ----------

        SixthSizer_vert = wx.BoxSizer(wx.VERTICAL) 
        SixthSizer_horiz1 = wx.BoxSizer(wx.HORIZONTAL) 
        
        SixthSizer_vert.AddSpacer(40)
        SixthSizer_horiz1.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz1)

        font61 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text61 = wx.StaticText(self, wx.ID_ANY, "Допустимое газосодержание при откачке нефтегазовой смеси по объему, %")
        text61.SetFont(font61)
        text61.SetForegroundColour('black')
        self.Show(True)
        
        txt61 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt61.Bind(wx.EVT_TEXT, self.onCheckSixTabFirstField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz1.Add(text61, flag = wx.ALL, border = 10)
        SixthSizer_horiz1.Add(txt61, flag = wx.ALL, border = 10)
        
#------ Второе поле ----------

        SixthSizer_horiz2 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz2.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz2) 

        font65 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')   
        text65 = wx.StaticText(self, wx.ID_ANY, "Толщина стенки НКТ, мм")
        text65.SetFont(font65)
        text65.SetForegroundColour('black')
        self.Show(True)
        
        txt65 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt65.Bind(wx.EVT_TEXT, self.onCheckSixTabSecondField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz2.Add(text65, flag = wx.ALL, border = 10)
        SixthSizer_horiz2.Add(txt65, flag = wx.ALL, border = 10)
        
        
#------ Третье поле ----------

        SixthSizer_horiz3 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz3.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz3) 

        font66 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text66 = wx.StaticText(self, wx.ID_ANY, "Толщина стенки ОК, мм")
        text66.SetFont(font66)
        text66.SetForegroundColour('black')
        self.Show(True)
        
        txt66 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt66.Bind(wx.EVT_TEXT, self.onCheckSixTabThirdField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz3.Add(text66, flag = wx.ALL, border = 10)
        SixthSizer_horiz3.Add(txt66, flag = wx.ALL, border = 10)
        
#------ Четвертое поле ----------  

        SixthSizer_horiz4 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz4.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz4) 
        
        font67 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text67 = wx.StaticText(self, wx.ID_ANY, "Теплоемкость нефти, Дж/кг*К")
        text67.SetFont(font67)
        text67.SetForegroundColour('black')
        self.Show(True)
        
        txt67 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
#         txt64 = wx.ComboBox(self, wx.ID_ANY, choices = ['', '1800'], style=wx.TE_CENTER)
        txt67.Bind(wx.EVT_TEXT, self.onCheckSixTabFourthField)
#         txt64.Bind(wx.EVT_COMBOBOX, self.onCheckSixTabFourthField)
        
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz4.Add(text67, flag = wx.ALL, border = 10)
        SixthSizer_horiz4.Add(txt67, flag = wx.ALL, border = 10)
        
#------ Пятое поле ----------

        SixthSizer_horiz5 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz5.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz5) 
        
        font68 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text68 = wx.StaticText(self, wx.ID_ANY, "Отношение длины верхней части к полной. 1 = одна ступень")
        text68.SetFont(font68)
        text68.SetForegroundColour('black')
        self.Show(True)
        
        txt68 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt68.Bind(wx.EVT_TEXT, self.onCheckSixTabFifthField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz5.Add(text68, flag = wx.ALL, border = 10)
        SixthSizer_horiz5.Add(txt68, flag = wx.ALL, border = 10)
        
        
#------ Шестое поле ----------

        SixthSizer_horiz6 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz6.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz6) 
        
        font69 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text69 = wx.StaticText(self, wx.ID_ANY, "Длина холодного конца, м")
        text69.SetFont(font69)
        text69.SetForegroundColour('black')
        self.Show(True)
        
        txt69 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt69.Bind(wx.EVT_TEXT, self.onCheckSixTabSixthField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz6.Add(text69, flag = wx.ALL, border = 10)
        SixthSizer_horiz6.Add(txt69, flag = wx.ALL, border = 10)
        
        
#------ Седьмое поле ----------
        
        SixthSizer_horiz7 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz7.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz7) 
        
        font610 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text610 = wx.StaticText(self, wx.ID_ANY, "Толщина термического сопротивления грунта, м")
        text610.SetFont(font610)
        text610.SetForegroundColour('black')
        self.Show(True)
        
        txt610 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt610.Bind(wx.EVT_TEXT, self.onCheckSixTabSeventhField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz7.Add(text610, flag = wx.ALL, border = 10)
        SixthSizer_horiz7.Add(txt610, flag = wx.ALL, border = 10)
        
        
#------ Восьмое поле ----------
        
        SixthSizer_horiz8 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz8.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz8) 
        
        font611 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text611 = wx.StaticText(self, wx.ID_ANY, "Запас по длине обогрева, м")
        text611.SetFont(font611)
        text611.SetForegroundColour('black')
        self.Show(True)
        
        txt611 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt611.Bind(wx.EVT_TEXT, self.onCheckSixTabEighthField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz8.Add(text611, flag = wx.ALL, border = 10)
        SixthSizer_horiz8.Add(txt611, flag = wx.ALL, border = 10)

#------ Девятое поле ----------

        SixthSizer_horiz9 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz9.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz9) 
        
        font612 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text612 = wx.StaticText(self, wx.ID_ANY, "Запас по минимальной температуре на выходе, град. С")
        text612.SetFont(font612)
        text612.SetForegroundColour('black')
        self.Show(True)
        
        txt612 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt612.Bind(wx.EVT_TEXT, self.onCheckSixTabNineField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz9.Add(text612, flag = wx.ALL, border = 10)
        SixthSizer_horiz9.Add(txt612, flag = wx.ALL, border = 10)
               
#------ Десятое поле ----------    

        SixthSizer_horiz10 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz10.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz10) 
           
        font613 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text613 = wx.StaticText(self, wx.ID_ANY, "Диапазон регулирования по температуре на выходе, град. С")
        text613.SetFont(font613)
        text613.SetForegroundColour('black')
        self.Show(True)
        
        txt613 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt613.Bind(wx.EVT_TEXT, self.onCheckSixTabTenthField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz10.Add(text613, flag = wx.ALL, border = 10)
        SixthSizer_horiz10.Add(txt613, flag = wx.ALL, border = 10)
                
#------ Одиннадцатое поле ----------  

        SixthSizer_horiz11 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz11.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz11) 

        font614 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text614 = wx.StaticText(self, wx.ID_ANY, "Диаметр кабеля, мм")
        text614.SetFont(font614)
        text614.SetForegroundColour('black')
        self.Show(True)
        
        txt614 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt614.Bind(wx.EVT_TEXT, self.onCheckSixTabEleventhField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz11.Add(text614, flag = wx.ALL, border = 10)
        SixthSizer_horiz11.Add(txt614, flag = wx.ALL, border = 10)

#------ Двенадцатое поле ----------

        SixthSizer_horiz12 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz12.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz12) 
        
        font615 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text615 = wx.StaticText(self, wx.ID_ANY, "Ручной выбор длины обогрева, м")
        text615.SetFont(font615)
        text615.SetForegroundColour('black')
        self.Show(True)
        
        txt615 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt615.Bind(wx.EVT_TEXT, self.onCheckSixTabTwelvethField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz12.Add(text615, flag = wx.ALL, border = 10)
        SixthSizer_horiz12.Add(txt615, flag = wx.ALL, border = 10)
        
#------ Тринадцатое поле ----------
        
        SixthSizer_horiz13 = wx.BoxSizer(wx.HORIZONTAL)
    
        SixthSizer_horiz13.AddSpacer(40)
        
        SixthSizer_vert.Add (SixthSizer_horiz13) 
        
        font616 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')  
        text616 = wx.StaticText(self, wx.ID_ANY, "Ручной выбор напряжения питания кабеля, В")
        text616.SetFont(font616)
        text616.SetForegroundColour('black')
        self.Show(True)
      
        txt616 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        txt616.Bind(wx.EVT_TEXT, self.onCheckSixTabThirtiethField)
        
        # Задаем дистанцию между текстом и полем 
        SixthSizer_horiz13.Add(text616, flag = wx.ALL, border = 10)
        SixthSizer_horiz13.Add(txt616, flag = wx.ALL, border = 10)
#-------------------------------------------------------------------------------------------------- 

        # Рисуем линию раздела
        wx.StaticLine(self, pos=(30, 670), size=(950,2))
        
        # Рисуем кнопки
        SixTabSaveButton = wx.Button(self, wx.ID_OK, label="Сохранить данные", pos=(50, 700))

        SixTabFutherButton = wx.Button(self, wx.ID_OK, label="Далее", pos=(530, 700))
        
        
        SixTabCloseButton = wx.Button(self, wx.ID_STOP, label="Закрыть", pos=(680, 700))
        
        # Сохраняем введенные данные
        SixTabSaveButton.Bind(wx.EVT_BUTTON, self.OnCheckSixthTab, SixTabSaveButton)
        SixTabCloseButton.Bind(wx.EVT_BUTTON, self.onCloseData, SixTabCloseButton)
        SixTabFutherButton.Bind(wx.EVT_BUTTON, self.onChoice, SixTabFutherButton)
        
        self.SetSizer(SixthSizer_vert)
        
#------------------------------------------------------------------------------------------------------
# делаем выбор по кнопке Далее

    def onChoice(self, event):
        
        """  """
        dlg = wx.MessageDialog(None, 'Данные были сохранены?', 'Сообщение', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        
        if result == wx.ID_YES:
            
            # Активность кнопки 'Ввод данных'  
            setDataPanel.EnableButton(ID_SetData, False)
            
            # готовим данные для расчета
            self.OnImportData(self)
            
            # Закрываем ноутбук    
            self.GetTopLevelParent().Destroy()  
            
        else:
            self.Close()
#-----------------------------------------------------------------------------------------------------------------        
# Закрываем окно ноутбука

    def onCloseData(self, event):
        
        """ Закрываем ноутбук с данными """   
        
        # Закрываем ноутбук    
        self.GetTopLevelParent().Destroy()        
#-----------------------------------------------------------------------------------------------------------------

# Готовим данные к расчету


    def OnImportData(self, event):
        
        """готовим анкетные данные для расчета """
        
        global thispath
        
#         # Считываем данные из файла
#         wildcard = "Text source (*.txt)|*.txt|" \
#             "All files (*.*)|*.*"
    
#         self.currentDirectory = os.getcwd()

#         dlg = wx.FileDialog(self, message="Открытие документа", defaultDir=self.currentDirectory, 
#                             defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)
        
#         if dlg.ShowModal() == wx.ID_OK:
            
#         thispath = dlg.GetPath()
            
        report = open(thispath, "r") 
            
        data_import = report.readlines()
            
        report.close()
 
        # удаляем строки заголовка с 0 по 16 строку 
        del data_import[0:15]
        
        # объединяем все значения в один список
        value = "".join(data_import)
    
        # разделяем список на части
        devOne = value.split()

        # удаляем весь лишний текст до первого значения
        del devOne[:3]

        # присваиваем значение переменным
        valueOne = devOne[0]
        valueTwo = devOne[7]
        valueThree = devOne[11]
        valueFour = devOne[16]
        valueFive = devOne[21]
        valueSix = devOne[28]
        valueSeven = devOne[35]
        valueEight = devOne[40]
        valueNine = devOne[48]
        valueTen = devOne[56]

        valueEleven = devOne[65]
        valueTwelve = devOne[73]
        valueThirteen = devOne[80]
        valueFourteen = devOne[85]
        valueFifteen = devOne[90]
        valueSixteen = devOne[99]
        valueSeventeen = devOne[104]
        valueEighteen = devOne[108]
        valueNineteen = devOne[116]
        valueTwenty = devOne[122]
        
        valueTwentyOne = devOne[127]
        valueTwentyTwo = devOne[136]
        valueTwentyThree = devOne[142]
        valueTwentyFour = devOne[150]
        valueTwentyFive = devOne[159]
        valueTwentySix = devOne[167]
        valueTwentySeven = devOne[172]
        valueTwentyEight = devOne[178]
        valueTwentyNine = devOne[184]
        valueThirty = devOne[191]

        valueThirtyOne = devOne[197] 
        valueThirtyTwo = devOne[204]
        valueThirtyThree = devOne[210] 
        valueThirtyFour = devOne[215]
        valueThirtyFive = devOne[220]
        valueThirtySix = devOne[231]
        valueThirtySeven = devOne[236]
        valueThirtyEight = devOne[241]
        valueThirtyNine = devOne[246]
        valueForty = devOne[251]

        valueFortyOne = devOne[256]
        valueFortyTwo = devOne[260]
        valueFortyThree = devOne[271]
        valueFortyFour = devOne[276]
        valueFortyFive = devOne[282]
        valueFortySix = devOne[288]
        valueFortySeven = devOne[296]
        valueFortyEight = devOne[304]
        valueFortyNine = devOne[308]
        valueFifty = devOne[314]

        valueFiftyOne = devOne[321]
 
        # преобразуем полученное значение в число
        num1 = float(valueOne)
        num2 = float(valueTwo)
        num3 = float(valueThree)
        num4 = float(valueFour)
        num5 = float(valueFive)
        num6 = float(valueSix)
        num7 = float(valueSeven)
        num8 = float(valueEight)
        num9 = float(valueNine)
        num10 = float(valueTen)
        
        num11 = float(valueEleven)
        num12 = float(valueTwelve)
        num13 = float(valueThirteen)
        num14 = float(valueFourteen)
        num15 = float(valueFifteen)
        num16 = float(valueSixteen)
        num17 = float(valueSeventeen)
        num18 = float(valueEighteen)
        num19 = float(valueNineteen)
        num20 = float(valueTwenty)
        
        num21 = float(valueTwentyOne)
        num22 = float(valueTwentyTwo)
        num23 = float(valueTwentyThree)
        num24 = float(valueTwentyFour)
        num25 = float(valueTwentyFive)
        num26 = float(valueTwentySix)
        num27 = float(valueTwentySeven)
        num28 = float(valueTwentyEight)
        num29 = float(valueTwentyNine)
        num30 = float(valueThirty)
        
        num31 = float(valueOne)
        num32 = float(valueThirtyTwo)
        num33 = float(valueThirtyThree)
        num34 = float(valueThirtyFour)
        num35 = float(valueThirtyFive)
        num36 = float(valueThirtySix)
        num37 = float(valueThirtySeven)
        num38 = float(valueThirtyEight)
        num39 = float(valueThirtyNine)
        num40 = float(valueForty)
        
        num41 = float(valueFortyOne)
        num42 = float(valueFortyTwo)
        num43 = float(valueFortyThree)
        num44 = float(valueFortyFour)
        num45 = float(valueFortyFive)
        num46 = float(valueFortySix)
        num47 = float(valueFortySeven)
        num48 = float(valueFortyEight)
        num49 = float(valueFortyNine)        
        num50 = float(valueFifty)
        num51 = float(valueFiftyOne)

        # создаем папку для временных файлов
        derictory = 'C:\Users\i.geraskin\Documents\Python script\Program\Temporary' 

        if not os.path.exists(derictory):  
            os.makedirs(derictory)

        # записываем результат в промежуточный файл

        f = open("C:\Users\i.geraskin\Documents\Python script\Program\Temporary\Treated_Data.txt", "w") 
        f.write(str(num1) + "\n")
        f.write(str(num2) + "\n")
        f.write(str(num3) + "\n")
        f.write(str(num4) + "\n")
        f.write(str(num5) + "\n")
        f.write(str(num6) + "\n")
        f.write(str(num7) + "\n")
        f.write(str(num8) + "\n")
        f.write(str(num9) + "\n")
        f.write(str(num10) + "\n")
        
        f.write(str(num11) + "\n")
        f.write(str(num12) + "\n")
        f.write(str(num13) + "\n")
        f.write(str(num14) + "\n")
        f.write(str(num15) + "\n")
        f.write(str(num16) + "\n")
        f.write(str(num17) + "\n")
        f.write(str(num18) + "\n")
        f.write(str(num19) + "\n")
        f.write(str(num20) + "\n")
        
        f.write(str(num21) + "\n")
        f.write(str(num22) + "\n")
        f.write(str(num23) + "\n")
        f.write(str(num24) + "\n")
        f.write(str(num25) + "\n")
        f.write(str(num26) + "\n")
        f.write(str(num27) + "\n")
        f.write(str(num28) + "\n")
        f.write(str(num29) + "\n")
        f.write(str(num30) + "\n")
        
        f.write(str(num31) + "\n")
        f.write(str(num32) + "\n")
        f.write(str(num33) + "\n")
        f.write(str(num34) + "\n")
        f.write(str(num35) + "\n")
        f.write(str(num36) + "\n")
        f.write(str(num37) + "\n")
        f.write(str(num38) + "\n")
        f.write(str(num39) + "\n")
        f.write(str(num40) + "\n")
        
        f.write(str(num41) + "\n")
        f.write(str(num42) + "\n")
        f.write(str(num43) + "\n")
        f.write(str(num44) + "\n")
        f.write(str(num45) + "\n")
        f.write(str(num46) + "\n")
        f.write(str(num47) + "\n")
        f.write(str(num48) + "\n")
        f.write(str(num49) + "\n")
        f.write(str(num50) + "\n") 
        f.write(str(num51))        
        f.close()

        # Считываем данные из промежуточного файла и присваиваем значения переменным,
        #                которые будут участвовать в расчете 
        
        path = "C:\Users\i.geraskin\Documents\Python script\Program\Temporary\Treated_Data.txt" 

        data = loadtxt(path, delimiter = " ", unpack=False)

        # Присваиваем значения переменным, которые будут участвовать в расчете
        
 #---------- Данные первой вкладки -----------#
        
        h_bhole = data[0]
        h_obs = data[1]
        d_vnesh_obs = data[2]
        h_nkt = data[3] 
        d_vnesh_nkt = data[4]
        h_stat = data[5]
        u_ESP = data[6]
        f_ESP = data[7]
        i_ESP = data[8]

#  --------- Данные второй вкладки ----------#

        t_bhole = data[9]
        h_ice = data[10]
        t_month = data[11] 
        t_maxh = data[12] 

#  -------- Данные третьей вкладки -----------#

        ro  = data[13]
        visc_plast = data[14]
        pn_plast = data[15]
        tkpn = data[16]
        g_plast = data[17]

#  -------- Данные четвертой вкладки ----------#

        nomdebit = data[18]
        debit_oil = data[19]  
        g = data[20]
        water = data[21]
        h_din = data[22]
        p_wellhead = data[23]
        t_wellhead = data[24]
        debit = data[25]
        scraper = data[26]
        h_aspo = data[27]

#-------- Данные пятой вкладки -------#

        ro_oil = data[28] 
        visc_oil = data[29]
        cp = data[30]
        asf = data[31]
        silica_gel = data[32]
        freezing_oil = data[33]
        t_0 = data[34]
        melting = data[35]
        ro_gas = data[36]
        ro_water = data[37]
        
 #-------- Данные шестой вкладки ---------#

        ESP_gas = data[38]
        d_vnut_nkt = data[39]
        d_vnut_obs = data[40]
        c_neft = data[41]
        kll = data[42]
        holkon = data[43]
        sh_gr = data[44]
        glub_zap = data[45]
        min_T_zap = data[46]
        ustavka = data[47]
        d_kab = data[48]
        long_ = data[49]
        u_u = data[50]
#------------------------------------------------------------------------------------------------------        
        
#         # Выводим сообщение об успешности сохранения
#         wx.MessageBox('Данные к расчету подготовленны!', 'Сообщение', wx.OK | wx.ICON_INFORMATION)
        
#         # Активность кнопки 'Импорт данных'  
#         ImportDataPanel.EnableButton(ID_ImportData, False)
        
        # Делаем активной кнопку пуска
        setCalcPanel.EnableButton(ID_Run, True)

#-----------------------------------------------------------------------------------------------------------------
        
# Проверяем заполнение полей шестой вкладки

    def OnCheckSixthTab(self, event):
        
        # Контрольные значения
        SixPointOne = txt61.GetValue()
        SixPointFive = txt65.GetValue()
        SixPointSix = txt66.GetValue()
        SixPointSeven = txt67.GetValue()
        SixPointEight = txt68.GetValue()
        SixPointNine = txt69.GetValue()
        SixPointTen = txt610.GetValue()
        SixPointEleven = txt611.GetValue()
        SixPointTwelve = txt612.GetValue()
        SixPointThirteen = txt613.GetValue()
        SixPointFourteen = txt614.GetValue()
        SixPointFifteen = txt615.GetValue()
        SixPointSixteen = txt616.GetValue()

        # Проверяем все ли поля заполнены    
        if SixPointOne and SixPointFive and SixPointSix and SixPointSeven and SixPointEight and SixPointNine and SixPointTen and SixPointEleven and SixPointTwelve and SixPointThirteen and SixPointFourteen and SixPointFifteen and SixPointSixteen != '': 
            # Если да - сохраняем анкетные данные
            self.CallofSaveData(self)       
        else:
            # Если нет - выводим предупреждающее сообщение
            wx.MessageBox('Чтобы сохранить данные, пожалуйста, заполните все пустые поля', 'Ошибка ввода данных', wx.OK | wx.ICON_ERROR)
#------------------------------------------------------------------------------------------------------------------------------
#
    def CallofSaveData(self, event):
        frame = onSaveAdditionalData(None)
        frame.Show()    
#-----------------------------------------------------------------------------------------------------------------

# Проверка первого поля

    def onCheckSixTabFirstField(self, event):
        
        """ Проверяем первое поле. 6.1 Допустимое газосодержание при откачке нефтегазовой смеси по объему. """

        # Задаем значения
        SixPointOne = txt61.GetValue() # допустимое газосодержание при откачке нефтегазовой смеси по объему
    
        # Делаем проверку 
        if SixPointOne == '':
            txt61.SetToolTip(wx.ToolTip("введите значение"))
        else:
            ESP_gas = str(SixPointOne)
            # Проверка на отрицательность значения
            if ESP_gas < '0':
                # Если значение вне диапазона
                txt61.SetForegroundColour(wx.RED)
                txt61.Refresh()
                # Выводим предупреждающую надпись    
                txt61.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение плотности"))     
            else:
                ESP_gas = float(SixPointOne)
                             
                if ESP_gas > 0 and ESP_gas <= 75:
                    txt61.SetForegroundColour(wx.BLACK)
                    txt61.Refresh()
                    txt61.SetToolTip(wx.ToolTip("")) 
                else:
                    # Если значение вне диапазона
                    txt61.SetForegroundColour(wx.RED)
                    txt61.Refresh()
                    # Выводим предупреждающую надпись    
                    txt61.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка второго поля

    def onCheckSixTabSecondField(self, event):
        
        """ Проверяем второе поле. 6.5 Внутренний диаметр НКТ. """

         # Задаем значения
        SixPointFive = txt65.GetValue() # 
    
        # Делаем проверку 
        if SixPointFive == '':
            txt65.SetToolTip(wx.ToolTip("введите значение"))
        else:
            d_vnut_nkt = str(SixPointFive)
            # Проверка на отрицательность значения
            if d_vnut_nkt < '0':
                # Если значение вне диапазона
                txt65.SetForegroundColour(wx.RED)
                txt65.Refresh()
                # Выводим предупреждающую надпись    
                txt65.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                d_vnut_nkt = float(SixPointFive)
                if d_vnut_nkt >=0 and d_vnut_nkt >= 5 and d_vnut_nkt <= 6:
                    txt65.SetForegroundColour(wx.BLACK)
                    txt65.Refresh()
                    txt65.SetToolTip(wx.ToolTip(""))
                else:
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt65.SetForegroundColour(wx.RED)
                    txt65.Refresh()
                    # Выводим предупреждающую надпись    
                    txt65.SetToolTip(wx.ToolTip("Внимание ошибка! Значение толщины находится вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка третьего поля

    def onCheckSixTabThirdField(self, event):
        
        """ Проверяем третье поле. 6.6 Внутренний диаметр обсадной трубы. """

        # Задаем значения
        SixPointSix = txt66.GetValue() # 
    
        # Делаем проверку 
        if SixPointSix == '':
            txt66.SetToolTip(wx.ToolTip("введите значение"))
        else:
            d_vnut_obs = str(SixPointSix)
            # Проверка на отрицательность значения
            if d_vnut_obs < '0':
                # Если значение вне диапазона
                txt66.SetForegroundColour(wx.RED)
                txt66.Refresh()
                # Выводим предупреждающую надпись    
                txt66.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                d_vnut_obs = float(SixPointSix)
                
                if d_vnut_obs >=0:
                    txt66.SetForegroundColour(wx.BLACK)
                    txt66.Refresh()
                    txt66.SetToolTip(wx.ToolTip(""))
                else:
                    # Если значение не в диапазоне, задаем красный цвет значения
                    txt66.SetForegroundColour(wx.RED)
                    txt66.Refresh()
                    # Выводим предупреждающую надпись    
                    txt66.SetToolTip(wx.ToolTip("Внимание ошибка! Значение толщины находится вне допустимого диапазона"))
#-----------------------------------------------------------------------------------------------------------------

# Проверка четвертого поля
    
    def onCheckSixTabFourthField(self, event):
        
        """ Проверяем четвертое поле. 6.7 Теплоемкость нефти. """

        # Задаем значения
        SixPointSeven = txt67.GetValue() # 
    
        # Делаем проверку 
        if SixPointSeven == '':
            txt67.SetToolTip(wx.ToolTip("введите значение"))
        else:
            c_neft = str(SixPointSeven)
            # Проверка на отрицательность значения
            if c_neft < '0':
                # Если значение вне диапазона
                txt67.SetForegroundColour(wx.RED)
                txt67.Refresh()
                # Выводим предупреждающую надпись    
                txt67.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                c_neft = float(SixPointSeven)
                if c_neft >=0:
                    txt67.SetForegroundColour(wx.BLACK)
                    txt67.Refresh()
                    txt67.SetToolTip(wx.ToolTip(""))    
#-----------------------------------------------------------------------------------------------------------------

# Проверка пятого поля

    def onCheckSixTabFifthField(self, event):
        
        """ Проверяем пятое поле. 6.8 Отношение длины верхней части к полной. """

        # Задаем значения
        SixPointEight = txt68.GetValue() # 
    
        # Делаем проверку 
        if SixPointEight == '':
            txt68.SetToolTip(wx.ToolTip("введите значение"))
        else:
            kll = str(SixPointEight)
            # Проверка на отрицательность значения
            if kll < '0':
                # Если значение вне диапазона
                txt68.SetForegroundColour(wx.RED)
                txt68.Refresh()
                # Выводим предупреждающую надпись    
                txt68.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                kll = float(SixPointEight)
                if kll >=0:
                    txt68.SetForegroundColour(wx.BLACK)
                    txt68.Refresh()
                    txt68.SetToolTip(wx.ToolTip(""))    
#-----------------------------------------------------------------------------------------------------------------

# Проверка шестого поля

    def onCheckSixTabSixthField(self, event):
        
        """ Проверяем шестое поле. 6.9 Длина холодного конца. """

        # Задаем значения
        SixPointNine = txt69.GetValue() # длина холодного конца
    
        # Делаем проверку 
        if SixPointNine == '':
            txt69.SetToolTip(wx.ToolTip("введите значение"))
        else:
            holkon = str(SixPointNine)
            # Проверка на отрицательность значения
            if holkon < '0':
                # Если значение вне диапазона
                txt69.SetForegroundColour(wx.RED)
                txt69.Refresh()
                # Выводим предупреждающую надпись    
                txt69.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                holkon = float(SixPointNine)
                if holkon >= 0:
                    txt69.SetForegroundColour(wx.BLACK)
                    txt69.Refresh()
                    txt69.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------

# Проверка седьмого поля

    def onCheckSixTabSeventhField(self, event):
        
        """ Проверяем седьмое поле. 6.10 Толщина термического сопротивления грунта. """

        # Задаем значения
        SixPointTen = txt610.GetValue() # 
    
        # Делаем проверку 
        if SixPointTen == '':
            txt610.SetToolTip(wx.ToolTip("введите значение"))
        else:
            sh_gr = str(SixPointTen)
            # Проверка на отрицательность значения
            if sh_gr < '0':
                # Если значение вне диапазона
                txt610.SetForegroundColour(wx.RED)
                txt610.Refresh()
                # Выводим предупреждающую надпись    
                txt610.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                sh_gr = float(SixPointTen)
                if sh_gr >= 0:
                    txt610.SetForegroundColour(wx.BLACK)
                    txt610.Refresh()
                    txt610.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------

# Проверка восьмого поля

    def onCheckSixTabEighthField(self, event):
        
        """ Проверяем восьмое поле. 6.11 Запас по длине обогрева. """

        # Задаем значения
        SixPointEleven = txt611.GetValue() # 
    
        # Делаем проверку 
        if SixPointEleven == '':
            txt611.SetToolTip(wx.ToolTip("введите значение"))
        else:
            glub_zap = str(SixPointEleven)
            # Проверка на отрицательность значения
            if glub_zap < '0':
                # Если значение вне диапазона
                txt611.SetForegroundColour(wx.RED)
                txt611.Refresh()
                # Выводим предупреждающую надпись    
                txt611.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                glub_zap = float(SixPointEleven)
                if glub_zap >= 0:
                    txt611.SetForegroundColour(wx.BLACK)
                    txt611.Refresh()
                    txt611.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------

# Проверка девятого поля

    def onCheckSixTabNineField(self, event):
        
        """ Проверяем девятое поле. 6.12 Запас по минимальной температуре на выходе. """

        # Задаем значения
        SixPointTwelve = txt612.GetValue() # 
    
        # Делаем проверку 
        if SixPointTwelve == '':
            txt612.SetToolTip(wx.ToolTip("введите значение"))
        else:
            min_T_zap = str(SixPointTwelve)
            # Проверка на отрицательность значения
            if min_T_zap < '0':
                # Если значение вне диапазона
                txt612.SetForegroundColour(wx.RED)
                txt612.Refresh()
                # Выводим предупреждающую надпись    
                txt612.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                min_T_zap = float(SixPointTwelve)
                if min_T_zap >= 0:
                    txt612.SetForegroundColour(wx.BLACK)
                    txt612.Refresh()
                    txt612.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------

# Проверка десятого поля

    def onCheckSixTabTenthField(self, event):
        
        """ Проверяем десятое поле. 6.13 Диапазон регулирования по температуре на выходе. """

        # Задаем значения
        SixPointThirteen = txt613.GetValue() # диапазон регулирования по температуре на выходе
    
        # Делаем проверку 
        if SixPointThirteen == '':
            txt613.SetToolTip(wx.ToolTip("введите значение"))
        else:
            ustavka = str(SixPointThirteen)
            # Проверка на отрицательность значения
            if ustavka < '0':
                # Если значение вне диапазона
                txt613.SetForegroundColour(wx.RED)
                txt613.Refresh()
                # Выводим предупреждающую надпись    
                txt613.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                ustavka = float(SixPointThirteen)
                if ustavka >=0:
                    txt613.SetForegroundColour(wx.BLACK)
                    txt613.Refresh()
                    txt613.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------
# Проверка одиннадцатого поля

    def onCheckSixTabEleventhField(self, event):
        
        """ Проверяем одиннадцатое поле. 6.14 Диаметр кабеля. """

        # Задаем значения
        SixPointFourteen = txt614.GetValue() # 
    
        # Делаем проверку 
        if SixPointFourteen == '':
            txt614.SetToolTip(wx.ToolTip("введите значение"))
        else:
            d_kab = str(SixPointFourteen)
            # Проверка на отрицательность значения
            if d_kab < '0':
                # Если значение вне диапазона
                txt614.SetForegroundColour(wx.RED)
                txt614.Refresh()
                # Выводим предупреждающую надпись    
                txt614.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                d_kab = float(SixPointFourteen)
                if d_kab >=0:
                    txt614.SetForegroundColour(wx.BLACK)
                    txt614.Refresh()
                    txt614.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------
# Проверка двенадцатого поля

    def onCheckSixTabTwelvethField(self, event):
        
        """ Проверяем двенадцатое поле. 6.15 Ручной выбор длины обогрева. """

        # Задаем значения
        SixPointFifteen = txt615.GetValue() # 
    
        # Делаем проверку 
        if SixPointFifteen == '':
            txt615.SetToolTip(wx.ToolTip("введите значение"))
        else:
            long_ = str(SixPointFifteen)
            # Проверка на отрицательность значения
            if long_ < '0':
                # Если значение вне диапазона
                txt615.SetForegroundColour(wx.RED)
                txt615.Refresh()
                # Выводим предупреждающую надпись    
                txt615.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                long_ = float(SixPointFifteen)
                if long_ >=0:
                    txt615.SetForegroundColour(wx.BLACK)
                    txt615.Refresh()
                    txt615.SetToolTip(wx.ToolTip(""))
#-----------------------------------------------------------------------------------------------------------------
# Проверка тринадцатого поля

    def onCheckSixTabThirtiethField(self, event):
        
        """ Проверяем тринадцатое поле. 6.16 Ручной выбор напряжения питания кабеля. """

        # Задаем значения
        SixPointSixteen = txt616.GetValue() # 
    
        # Делаем проверку 
        if SixPointSixteen == '':
            txt616.SetToolTip(wx.ToolTip("введите значение"))
        else:
            u_u = str(SixPointSixteen)
            # Проверка на отрицательность значения
            if u_u < '0':
                # Если значение вне диапазона
                txt616.SetForegroundColour(wx.RED)
                txt616.Refresh()
                # Выводим предупреждающую надпись    
                txt616.SetToolTip(wx.ToolTip("Внимание ошибка! Введено отрицательное значение"))     
            else:
                u_u = float(SixPointSixteen)
                if u_u >=0:
                    txt616.SetForegroundColour(wx.BLACK)
                    txt616.Refresh()
                    txt616.SetToolTip(wx.ToolTip(""))
                    
####################################################################################################################
class NotebookFrame(wx.Frame):
    
    """  создаем ноутбук с данными  """
    
#---------------------------------------------------------------------------------------------------------------
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Ввод данных для расчета", pos=wx.DefaultPosition,
                          size=wx.Size(820, 820), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        
#------------------ Добавляем иконку в верхний левый угол главного окна ----------------------------

        # Размещаем картинку
        icon = wx.Icon('C:\Users\i.geraskin\Documents\Python script\Program\Add_data.png', wx.BITMAP_TYPE_PNG)
        # Показываем в окне
        self.SetIcon(icon)
        
        style = aui.AUI_NB_DEFAULT_STYLE ^ aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
        
        mgr = aui.AuiManager()

        # tell AuiManager to manage this frame
        mgr.SetManagedWindow(self)


        # Устанавливаем свойства
        self.notebook = aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, agwStyle = style)
        
        # Рисуем вкладки      
        tab1 = TabPanelOne(self.notebook)
        tab2 = TabPanelTwo(self.notebook)
        tab3 = TabPanelThree(self.notebook)
 
        tab4 = TabPanelFour(self.notebook)
        tab5 = TabPanelFive(self.notebook)
        tab6 = TabPanelSix(self.notebook)

        # Называем вкладки
        self.notebook.AddPage(tab1, "Лифтовое оборудование", False)
        self.notebook.AddPage(tab2, "Окружающая среда", False)
        self.notebook.AddPage(tab3, "Пластовой флюид", False)
        
        self.notebook.AddPage(tab4, "Скважина", False)
        self.notebook.AddPage(tab5, "Нефть", False)
        self.notebook.AddPage(tab6, "Дополнительные параметры", False)
        
        mgr.AddPane(self.notebook, aui.AuiPaneInfo().Name("notebook_content").CenterPane().PaneBorder(True))
        mgr.Update()
    
        
    # Управляем активностью вкладок 
               
        # Доступность вкладок
        """ True - вкладка активна, False - нет"""

        # Первая вкладка
        self.notebook.EnableTab(0, True)
        
        # Вторая вкладка
        self.notebook.EnableTab(1, True)
        
        # Третья вкладка
        self.notebook.EnableTab(2, True)
        
        # Четвертая вкладка
        self.notebook.EnableTab(3, True)
        
        # Пятая вкладка
        self.notebook.EnableTab(4, True)
        
        # Шестая вкладка
        self.notebook.EnableTab(5, True)
        
#************************************* Рисуем боксы ********************************************************
# Первая вкладка

 # Общий бокс для первого бокса
    
        fontlabel = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas') 
        Label = wx.StaticBox(tab1, label='1. ОБЩИЕ СВЕДЕНИЯ', pos=(10, 50), size=(610, 370))
        Label.SetFont(fontlabel)
        Label.SetForegroundColour('BLUE')
        self.Show(True)
    
  # Рисуем первый бокс     
        fontlabel1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas') 
        Label1 = wx.StaticBox(tab1, label='ЭКСПЛУАТАЦИОННАЯ КОЛОННА', pos=(20, 70), size=(550, 160))
        Label1.SetFont(fontlabel1)
        Label1.SetForegroundColour('BLUE')
        self.Show(True)

  # Рисуем второй бокс

        fontlabel11 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')  
        Label2 = wx.StaticBox(tab1, label='НКТ', pos=(120, 250), size=(480, 150))
        Label2.SetFont(fontlabel11)
        Label2.SetForegroundColour('BLUE')
        self.Show(True)        

  # Рисуем третий бокс
        fontlabel111 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')  
        Label3 = wx.StaticBox(tab1, label='6. ХАРАКТЕРИСТИКИ НАСОСНОГО ОБОРУДОВАНИЯ', pos=(220, 470), size=(430, 160))
        Label3.SetFont(fontlabel111)
        Label3.SetForegroundColour('BLUE')
        self.Show(True)         
#---------------------------------------------------------------------------------------------------------
# Вторая вкладка

        fontlabel2 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')  
      
        Label4 = wx.StaticBox(tab2, label='2. РАСПРЕДЕЛЕНИЕ ТЕМПЕРАТУР ПО ГЛУБИНЕ', pos=(95, 35), size=(620, 200))
        
        Label4.SetFont(fontlabel2)
        Label4.SetForegroundColour('BLUE')
        self.Show(True)
        
#------------------------------------------------------------------------------------------------------------   
# Третья вкладка

        fontlabel3 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')  

        Label5 = wx.StaticBox(tab3, label='3. ХАРАКТЕРИСТИКИ ПЛАСТОВОЙ ЖИДКОСТИ', pos=(60, 40), size=(570, 260))
        Label5.SetFont(fontlabel3)
        Label5.SetForegroundColour('BLUE')
        self.Show(True)
#----------------------------------------------------------------------------------------------------------------        
# Четвертая вкладка

        fontlabel4 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')  

        Label6 = wx.StaticBox(tab4, label='4. РЕЖИМ ЭКСПЛУАТАЦИИ СКВАЖИНЫ', pos=(40, 30), size=(600, 540))
        Label6.SetFont(fontlabel4)
        Label6.SetForegroundColour('BLUE')
        self.Show(True)
#---------------------------------------------------------------------------------------------------------------
# Пятая вкладка

        fontlabel5 = wx.Font(10, wx.MODERN, wx.NORMAL,  wx.BOLD, False, u'Consolas')  

        Label7 = wx.StaticBox(tab5, label='5. ХАРАКТЕРИСТИКА СЕПАРИРОВАННОЙ НЕФТИ', pos=(40, 20), size=(600, 550))
        Label7.SetFont(fontlabel5)
        Label7.SetForegroundColour('BLUE')
        self.Show(True)
        
#---------------------------------------------------------------------------------------------------------------        
# Шестая вкладка

        fontlabel6 = wx.Font(10, wx.MODERN, wx.NORMAL,  wx.BOLD, False, u'Consolas')  

        Label8 = wx.StaticBox(tab6, label='6. ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ', pos=(30, 20), size=(740, 590))
        Label8.SetFont(fontlabel6)
        Label8.SetForegroundColour('BLUE')
        self.Show(True)
        
        
############################################################################################################

class onSaveAdditionalData(wx.Dialog):
    
    """ Создаем дополнительное окно с дополнением к анкете """
    
#------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(onSaveAdditionalData, self).__init__(*args, **kwargs)
        
        self.InitUI()
        
#------------------------------------------------------------------------------------------        
    def InitUI(self):
        
        global SaveButton #, ImportButton 

        self.SetSize((370, 350))
        self.SetTitle('Данные по месторождению')
        self.Centre()
        
        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory = os.getcwd()
        
        wx.StaticText(panel, wx.ID_ANY, "Оператор:", pos=(20, 20)) 
        wx.StaticText(panel, wx.ID_ANY, "Название месторождения:", pos=(20, 70))       
        wx.StaticText(panel, wx.ID_ANY, "Номер скважины:", pos=(20, 120)) 
        self.esp = wx.StaticText(panel, wx.ID_ANY, "Марка ЭЦН:", pos=(20, 175))

        
        self.posCtrl1 = wx.TextCtrl(panel, wx.ID_ANY, "", pos=(90, 20))
        self.posCtrl2 = wx.TextCtrl(panel, wx.ID_ANY, "", pos=(180, 70))
        self.posCtrl3 = wx.TextCtrl(panel, wx.ID_ANY, "", pos=(130, 120))
        self.ESPname = wx.TextCtrl(panel, wx.ID_ANY, "", pos=(110, 175))
  
        SaveButton = wx.Button(panel,label = "Сохранить", pos=(150,270))
        self.button3 = wx.Button(panel,label = "Закрыть", pos=(260,270))
        
        # Выключаем кнопку 'Создать отчет'
        SaveButton.Enable()
        
        # Сохраняем данные окна
        self.Bind(wx.EVT_BUTTON, self.onSave_Worksheet_DataAs, SaveButton)
        
        # Закрываем тоутбук
        self.Bind(wx.EVT_BUTTON, self.onClose, self.button3)
        
  # Сохраняем данные ноутбука

    def onSave_Worksheet_DataAs(self, event):
        
        """ Сохранение анкетных данных """
        
        global thispath

        wildcard = "Text source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
    
        self.currentDirectory = os.getcwd()

        dlg = wx.FileDialog(self, message="Сохранение анкетных данных", defaultDir=self.currentDirectory, 
                            defaultFile="", wildcard=wildcard, style=wx.FD_SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            
            thispath = dlg.GetPath()
            
            report = open(thispath, "w") 
 #----------------------------------------------------------------------------------------------------------------
 # Считываем значения с полей
        
        """ Ниже приводится список переменных, участвующих в расчетах (цифра - номер пункта анкеты):
        
        ********************************************************************************        
            h_bhole - 1.4 глубина забоя, м
            h_obs - 1.5 Длина эксплуатационной колонны, м
            d_vnesh_obs - 1.6 Диаметр эксплуатационной колонны,м
            h_nkt - 1.7 Длина колонны НКТ, м
            d_vnesh_nkt - 1.8 Диаметр колонны НКТ, м
            h_stat - 1.9 Статический уровень флюида в скважине, м
            
         ******************************************************************************   
            t_bhole - 2.1 Температура нефтяного пласта, град С
            h_ice - 2.2 Глубина вечномерзлых грунтов, м
            t_month - 2.3 Средняя температура наиболее холодного месяца, град С
            t_maxh - 2.4 Максимальная температура наиболее теплого месяца, град С
            
        ******************************************************************************    
            ro - 3.1 Плотность нефтяного флюида в условиях пласта, кг/м3
            visc_plast - 3.2 Вязкость нефтяного флюида в условиях пласта, мПа*с
            pn_plast - 3.3 Давление насыщения в условиях пласта, МПа
            tkpn - 3.4 Температурный коэффициент давления насыщения
            g_plast - 3.5 Газосодержание пластовой жидкости, м3/м3
        
        *******************************************************************************
            nomdebit - 4.1 Дебит по жидкости (с чистой НКТ), м3/сут
    
            debit_oil - 4.2 Дебит по нефти, т/сут
            g - 4.3 Газовый фактор, м3/м3
            water - 4.4 Содержание воды, массовая доля,% по массе
            h_din - 4.5 Динамический уровень, м от устья
            p_wellhead - 4.6 Давление на устье, МПа
    
            t_wellhead - 4.7 Температура жидкости на выходе из скважины, град С
            debit - 4.8 Минимальный дебит по жидкости м3/сут
            scraper - 4.9 Глубина спуска скребка при механической очистке, м
            h_aspo - 4.10 Максимальная глубина отложения АСПО (по данным КРС), м
                
        ***********************************************************************************
            ro_oil - 5.1 Плотность дегазированной нефти в норм. условиях,кг/м3
            visc_oil - 5.2 Вязкость дегазированной нефти, мПа*с
            cp - 5.3 Содержание парафина, массовая доля, %
            asf - 5.4 Содержание асфальтенов, массовая доля, %
            silica_gel - 5.5 Содержание смол силикагелевых, массовая доля, %
            freezing_oil - 5.6 Температура застывания нефти, град С
            t_0 - 5.7 Температура насыщения нефти парафином, град С
            melting - 5.8 Температура плавления парафинов, град С
            ro_gas - 5.9 Плотность сопутствующего газа, кг/м3
            ro_water - 5.10 Плотность сопутствующей воды, кг/м3
        
        *******************************************************************************************
            ESP_gas - 6.1 Допустимое газосодержание при откачке нефтегазовой смеси по объему, %
            
            u_ESP - 6.2 Напряжение питания ПЭД, В
            
            f_ESP - 6.3 Частота питающего напряжения, Гц
            
            i_ESP - 6.4 Ток потребления ПЭД, А            
          
             d_vnut_nkt - 6.5 Внутренний диаметр нкт, м
            d_vnut_obs - 6.6 Внутренний диаметр обсадной трубы, м
            c_neft - 6.7 Теплоемкость нефти, Дж/кг·К
            kll - 6.8 Отношение длины верхней части к полной. 1 = одна ступень
            holkon - 6.9 Длина холодного конца, м
            sh_gr - 6.10 Толщина термического сопротивления грунта, м
            glub_zap - 6.11 Запас по длине обогрева, м
            min_T_zap - 6.12 Запас по минимальной температуре на выходе, °С
            ustavka - 6.13 Диапазон регулирования по температуре на выходе, °С
            d_kab - 6.14 Диаметр кабеля, м
            long - 6.15 Ручной выбор длины обогрева, м
            u_u - 6.16 Ручной выбор напряжения питания кабеля, В
            
        ***********************************************************************************************
        
        """
# --------------------------- Определяем переменные ---------------------------------------
   # Данные первой вкладки
    
        h_bhole = float(txt14.GetValue())
        h_obs = float(txt15.GetValue())
        d_vnesh_obs = float(txt16.GetValue())
        h_nkt  = float(txt17.GetValue())
        d_vnesh_nkt = float(txt18.GetValue())
        h_stat = float(txt19.GetValue())
        
   # Данные второй вкладки

        t_bhole = float(txt21.GetValue())
        h_ice = float(txt22.GetValue())
        t_month = float(txt23.GetValue())
        t_maxh = float(txt24.GetValue())

   # Данные третьей вкладки

        ro = float(txt31.GetValue())
        visc_plast = float(txt32.GetValue())
        pn_plast = float(txt33.GetValue())
        tkpn = float(txt34.GetValue())
        g_plast = float(txt35.GetValue())

   # Данные четвертой вкладки

        nomdebit = float(txt41.GetValue())
        debit_oil  = float(txt42.GetValue())
        g = float(txt43.GetValue())
        water = float(txt44.GetValue())
        h_din = float(txt45.GetValue())
        p_wellhead = float(txt46.GetValue())
        t_wellhead = float(txt47.GetValue())
        debit = float(txt48.GetValue())
        scraper = float(txt49.GetValue())
        h_aspo = float(txt410.GetValue())

   # Данные пятой вкладки

        ro_oil  = float(txt51.GetValue())
        visc_oil = float(txt52.GetValue())
        cp = float(txt53.GetValue())
        asf = float(txt54.GetValue())
        silica_gel = float(txt55.GetValue())
        freezing_oil = float(txt56.GetValue())
        t_0 = float(txt57.GetValue())
        melting = float(txt58.GetValue())
        ro_gas = float(txt59.GetValue())
        ro_water = float(txt510.GetValue())

   # Данные шестой вкладки

        ESP_gas = float(txt61.GetValue())
        u_ESP = float(txt62.GetValue())
        f_ESP = float(txt63.GetValue())
        i_ESP = float(txt64.GetValue())
        d_vnut_nkt = float(txt65.GetValue())
        d_vnut_obs = float(txt66.GetValue())
        c_neft = float(txt67.GetValue())
        kll = float(txt68.GetValue())
        holkon = float(txt69.GetValue())
        sh_gr = float(txt610.GetValue())
        glub_zap = float(txt611.GetValue())
        min_T_zap = float(txt612.GetValue())
        ustavka = float(txt613.GetValue())
        d_kab = float(txt614.GetValue())
        long_ = float(txt615.GetValue())
        u_u = float(txt616.GetValue())

        operator = str(self.posCtrl1.GetValue())
        name = str(self.posCtrl2.GetValue())
        number = str(self.posCtrl3.GetValue())
        self.label = str(self.ESPname.GetValue())
        
            # Создаем заголовочный файл

            # Устанавливаем дату и время
        date = strftime("%a %d-%m-%y %H:%M:%S")

        # Добавляем линию конца заголовочного файла
        div = '********************** Конец заголовка ***************************'
        
        div2 = '*****************************************************************'
       
        report.write('Сохраненные анкетные данные')
                
        report.write('\n')
        
        report.write('\n Разработчик: ООО ОКБ "Гамма"')
        
        report.write('\n')
        
        report.write('\n Дата сохранения: ' + date)
        
        report.write('\n')
        
        report.write('\n Оператор: %s' % operator)
        
        report.write('\n')
        
        report.write('\n Наименование месторождения: %s' % name)
        
        report.write('\n')
        
        report.write('\n Номер скважины: %s' % number)
        
        report.write('\n')
               
        report.write('\n Погружной ЭЦН марки: %s ' % self.label)
        
        report.write('\n')
        
        report.write('\n' + div * 1 + '\n')
        
#---------------------------- Данные первой вкладки ----------------------------------------------
        
        report.write('\n Глубина забоя, м: %s' % h_bhole)
        
        report.write('\n')
        
        report.write('\n Длина эксплуатационной колонны (с хвостовиком), м: %s' % h_obs)
            
        report.write('\n')
          
        report.write('\n Диаметр эксплуатационной колонны,м: %s' % d_vnesh_obs)
            
        report.write('\n')
        
        report.write('\n Длина колонны НКТ, м: %s' % h_nkt)
            
        report.write('\n')
        
        report.write('\n Диаметр колонны НКТ, м: %s' % d_vnesh_nkt)
            
        report.write('\n')
        
        report.write('\n Статический уровень флюида в скважине, м: %s' % h_stat)
            
        report.write('\n')
        
        report.write('\n' + div2 * 1 + '\n')
                   
#---------------------------- Данные второй вкладки ----------------------------------------------   

        report.write('\n Температура нефтяного пласта, град С: %s' % t_bhole)
            
        report.write('\n')

        report.write('\n Глубина вечномерзлых грунтов, м: %s' %  h_ice)
            
        report.write('\n')
        
        report.write('\n Средняя температура наиболее холодного месяца, град С: %s' % t_month)
            
        report.write('\n')
        
        report.write('\n Максимальная температура наиболее теплого месяца, град С: %s' % t_maxh)
        
        report.write('\n')
        
        report.write('\n' + div2 * 1 + '\n')
            
#---------------------------- Данные третьей вкладки ----------------------------------------------

        report.write('\n Плотность нефтяного флюида в условиях пласта, кг/м3: %s' % ro)
            
        report.write('\n')
        
        report.write('\n Вязкость нефтяного флюида в условиях пласта, мПа*с: %s' % visc_plast)
            
        report.write('\n')
        
        report.write('\n Давление насыщения в условиях пласта, МПа: %s' % pn_plast)
            
        report.write('\n')
        
        report.write('\n Температурный коэффициент давления насыщения: %s' % tkpn)
            
        report.write('\n')
        
        report.write('\n Газосодержание пластовой жидкости, м3/м3: %s' % g_plast)
        
        report.write('\n')
        
        report.write('\n' + div2 * 1 + '\n')
            
#---------------------------- Данные четвертой вкладки ------------------------------------------------

        report.write('\n Дебит по жидкости (с чистой НКТ), м3/сут: %s' % nomdebit)
            
        report.write('\n')
        
        report.write('\n Дебит по нефти, т/сут: %s' % debit_oil)
            
        report.write('\n')
        
        report.write('\n Газовый фактор, м3/м3: %s' % g)
            
        report.write('\n')
        
        report.write('\n Содержание воды, массовая доля, проц. по массе: %s' % water)
            
        report.write('\n')
        
        report.write('\n Динамический уровень, м от устья: %s' % h_din)
            
        report.write('\n')
        
        report.write('\n Давление на устье, МПа: %s' % p_wellhead)
            
        report.write('\n')
        
        report.write('\n Температура жидкости на выходе из скважины, град С: %s' % t_wellhead)
            
        report.write('\n')
        
        report.write('\n Минимальный дебит по жидкости м3/сут: %s' % debit)
            
        report.write('\n')
        
        report.write('\n Глубина спуска скребка при механической очистке, м: %s' % scraper)
            
        report.write('\n')
        
        report.write('\n Максимальная глубина отложения АСПО (по данным КРС), м: %s' % h_aspo)
        
        report.write('\n')
        
        report.write('\n' + div2 * 1 + '\n')
            
#---------------------------- Данные пятой вкладки ----------------------------------------------------

        report.write('\n Плотность дегазированной нефти в норм. условиях,кг/м3: %s' % ro_oil)
            
        report.write('\n')
        
        report.write('\n Вязкость дегазированной нефти, мПа*с: %s' % visc_oil)
            
        report.write('\n')
        
        report.write('\n Содержание парафина, массовая доля, проц.: %s' % cp)
            
        report.write('\n')
        
        report.write('\n Содержание асфальтенов, массовая доля, проц.: %s' % asf)
            
        report.write('\n')
        
        report.write('\n Содержание смол силикагелевых, массовая доля, проц.: %s' % silica_gel)
            
        report.write('\n')
        
        report.write('\n Температура застывания нефти, град С: %s' % freezing_oil)
            
        report.write('\n')
        
        report.write('\n Температура насыщения нефти парафином, град С: %s' % t_0)
            
        report.write('\n')
        
        report.write('\n Температура плавления парафинов, град С: %s' % melting)
            
        report.write('\n')
        
        report.write('\n Плотность сопутствующего газа, кг/м3: %s' % ro_gas)
            
        report.write('\n')
        
        report.write('\n Плотность сопутствующей воды, кг/м3: %s' % ro_water)
        
        report.write('\n')
        
        report.write('\n' + div2 * 1 + '\n')
            
#---------------------------- Данные шестой вкладки ----------------------------------------------------  

        report.write('\n Допустимое газосодержание при откачке нефтегазовой смеси по объему, проц.: %s' % ESP_gas)
            
        report.write('\n')
        
        report.write('\n Напряжение питания ПЭД, В: %s' % u_ESP)
            
        report.write('\n')
        
        report.write('\n Частота питающего напряжения, Гц: %s' % f_ESP)
            
        report.write('\n')
        
        report.write('\n Ток потребления ПЭД, А: %s' % i_ESP)
        
        report.write('\n')
            
        report.write('\n Толщина стенки НКТ, мм: %s' % d_vnut_nkt)
        
        report.write('\n')
        
        report.write('\n Толщина стенки ОК, мм: %s' % d_vnut_obs)
            
        report.write('\n')
        
        report.write('\n Теплоемкость нефти, Дж/кг·К: %s' % c_neft)
            
        report.write('\n')
        
        report.write('\n Отношение длины верхней части к полной. 1 = одна ступень: %s' % kll)
            
        report.write('\n')
        
        report.write('\n Длина холодного конца, м: %s' % holkon)
            
        report.write('\n')
        
        report.write('\n Толщина термического сопротивления грунта, м: %s' % sh_gr)
            
        report.write('\n')
        
        report.write('\n Запас по длине обогрева, м: %s' % glub_zap)
            
        report.write('\n')
        
        report.write('\n Запас по минимальной температуре на выходе, °С: %s' % min_T_zap)
            
        report.write('\n')
        
        report.write('\n Диапазон регулирования по температуре на выходе, °С: %s' % ustavka)
            
        report.write('\n')
        
        report.write('\n Диаметр кабеля, мм: %s' % d_kab)
            
        report.write('\n')
        
        report.write('\n Ручной выбор длины обогрева, м: %s' % long_)
            
        report.write('\n')
        
        report.write('\n Ручной выбор напряжения питания кабеля, В: %s' % u_u)
            
        report.write('\n')
        
        report.write('\n' + div2 * 1 + '\n')
#--------------------------------------------------------------------------------------------------------

        # Закрываем файл после записи
        report.close()
    
        SaveButton.Disable()
        
#         self.OnImportData()
        
        
        # Выводим сообщение об успешности сохранения
        wx.MessageBox('Анкетные данные успешно сохранены!', 'Сохранение', wx.OK | wx.ICON_INFORMATION)

#-------------------------------------------------------------------------------------------------------
    def onClose(self, event):
        
        """ закрываем окно с данными по месторождению """
        
        self.Close()

##################################################################################################  
#--------------------------------- ProgressBar и Расчет -----------------------------------------#
##################################################################################################

class MyProgressDialog(wx.ProgressDialog):
    
    """  """   
    
    H = 3137 # задаем глубину до забоя
#------------------------------------------------------------------------------------    
    def __init__(self):
        wx.ProgressDialog.__init__(self, "Выполняется расчет", "Пожалуйста, подождите...", self.H, style=wx.PD_CAN_ABORT|wx.PD_SMOOTH|wx.PD_AUTO_HIDE)
#-------------------------------------------------------------------------------------
    def Show(self):
        global x
        keepGoing = True
        
        # задаем пустой список
        b =[]
        
        # задаем начальное значение шага
        h = 0 # начальный уровень от устья скважины           
            
        while keepGoing and h < self.H:
            b.append(h)
            x = np.asarray(b)
            # задаем местоположение файла
            path = 'Data\Temporary\depth.txt'
            
            # записываем результат в промежуточный файл            
            np.savetxt(path, x, fmt = '%4.1f', delimiter = ' ')
            
            h += 1 # задаем шаг 1 м
            
            wx.Sleep(0.01)
            keepGoing = self.Update(h)           
#------------------------------------------------------------------------------------
      
##################################################################################################  
#---------------------------------------- 'Просмотра отчета' ------------------------------------#
##################################################################################################

class Viewer(wx.Frame):
    
    #---------------------------------------------------------------------------------------------------        
    def OnOpenFile(self, event):
        
        # This is how you pre-establish a file filter so that the dialog
        # only shows the extension(s) you want it to.
        
#         wildcard = 'Python source (*.py)|*.py'
        wildcard = 'Text source (*.txt)|*.txt'
        
        dlg = wx.FileDialog(None, message="Выбор файла", defaultDir=os.getcwd(), 
                            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns the file that was selected
            path = dlg.GetPath()

            # Open the file as read-only and slurp its content
            fid = open(path, 'rt')
            text = fid.read()
            fid.close()

            text_ctrl = wx.TextCtrl(self.notebook, style=wx.TE_MULTILINE)
            text_ctrl.SetFont(wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
            text_ctrl.SetValue(text)

            filename = os.path.split(os.path.splitext(path)[0])[1]
            self.notebook.AddPage(text_ctrl, filename, select=True)

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwtwise!
        dlg.Destroy()

#----------------------------------------------------------------------------------------------    
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title, size = (600, 500))
        
        style = aui.AUI_NB_DEFAULT_STYLE ^ wx.aui.AUI_NB_BOTTOM

        # Create the notebook 
             
        mgr = aui.AuiManager()

        # tell AuiManager to manage this frame
        mgr.SetManagedWindow(self)

        self.notebook = aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, agwStyle=style) 
    
        # Добавляем иконку в верхний левый угол главного окна        
        # Размещаем картинку
        icon = wx.Icon('Picture\Viewer.png', wx.BITMAP_TYPE_PNG)
        # Показываем в окне
        self.SetIcon(icon)

        # Creating the menubar
        menu_bar = wx.MenuBar()

        # Setting up the menu
        file_menu = wx.Menu()
        # wx.ID_OPEN
        menu_item = file_menu.Append(wx.ID_OPEN, '&Открыть...\tCtrl+N', 'выбираем нужный файл ')
        
        # Bind the "select menu item" event to the OnOpen event handler
        self.Bind(wx.EVT_MENU, self.OnOpenFile, menu_item)
    

        # Adding the 'file_menu' to the menu bar
        menu_bar.Append(file_menu, '&Файл')
        file_menu.AppendSeparator()
      
        qmi = wx.MenuItem(file_menu, wx.ID_EXIT, '&Выход\tCtrl+Q', 'входим из программы')
        file_menu.Append(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuitViewer, qmi)
        
        # Adding the menu bar to the frame content
        self.SetMenuBar(menu_bar)
        self.Center()
        self.Show()
        
        # Создаем строку состояния StatusBar
        self.CreateStatusBar()
        
        # Выводим в нем приветствие
        self.PushStatusText("Добро пожаловать! выбирете меню Файл чтобы открыть файл")
        

#------------------------------------------------------------------------------------------------        
    def OnQuitViewer(self, event):
        self.Close()
        
##################################################################################################  
#--------------------------------------- 'Построить график' -------------------------------------#
##################################################################################################

class PlotFrame(wx.Frame):
   
    help_msg = """  Пункты меню:
     Сохранить                       экспорт рисунка графика (png, eps, bmp, jpg) в файл
     Копировать                      копировать изображение графика в системный буфер обмена
     Настройка печати                настройка размера страницы для печати
     Предварительный просмотр        предварительный просмотр страницы для печати
     Печать                          отправить график на печать на текущий принтер
     Выход                           выход из приложения
  
     где 'рисунок' означает изображение, построенное с помощью библиотеки matplotlib canvas
  
  В добавок, нажатие сочетания клавиш "Ctrl-C" позволяют сохранить изображение в системном буфере обмена
"""
  
    start_msg  = """        воспользуйтесь Меню для печати
        или Ctrl-C чтобы сохранить изображение """
  
    about_msg =  """    распечатано из wx версия 0.1  03-Aug-2018
        Гераськин Игорь <i.geraskin@okb-gamma.ru>"""
#---------------------------------------------------------------------------------------  
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Результирующий график")              
        self.fig  = Figure((5.0, 3.0), dpi = 100)
        self.canvas = FigCanvas(self, -1, self.fig)
        self.axes = self.fig.add_axes([0.15, 0.15, 0.75, 0.75])
        
        self.print_data = wx.PrintData()
        self.clip = wx.Clipboard()
        self.x = wx.BitmapDataObject()
        
        #imageFile = 'export_plot.jpg'
        #self.bmp = wx.Bitmap(imageFile)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.LEFT|wx.TOP|wx.GROW)
        sizer.Add(wx.StaticText(self,-1, self.start_msg), 0, wx.ALIGN_LEFT|wx.TOP)
  
        self.canvas.Bind(wx.EVT_KEY_DOWN, self.onKeyEvent)
    
        # Добавляем иконку в верхний левый угол главного окна        
        # Размещаем картинку
        icon = wx.Icon('Picture\Graph.png', wx.BITMAP_TYPE_PNG)
        # Показываем в окне
        self.SetIcon(icon)
  
        self.SetSizer(sizer)
        self.Fit()
        self.Build_Menus()
        self.Plot_Data()
#------------------------------------------------------------------------------------------  
    def Build_Menus(self):
        
        """ создаем меню """
        
        MENU_EXIT  = wx.NewIdRef()
        MENU_SAVE  = wx.NewIdRef()
        MENU_PRINT = wx.NewIdRef()
        MENU_PSETUP = wx.NewIdRef()
        MENU_PREVIEW = wx.NewIdRef()
        MENU_CLIPB = wx.NewIdRef()
        MENU_REPORT = wx.NewIdRef()
        MENU_FILE_REPORT = wx.NewIdRef()
        MENU_HELP = wx.NewIdRef()
  
        # Рисуем меню
        menuBar = wx.MenuBar()
        
        # Меню 'Файл'
        f0 = wx.Menu()
        f0.Append(MENU_SAVE, "Экспорт изображения", "Сохранить изображение графика")
        f0.AppendSeparator()
        f0.Append(MENU_PSETUP, "Настройка страницы...", "Настройка принтера")
        f0.Append(MENU_PREVIEW,"Предварительный просмотр...", "Предварительный просмотр")
        f0.Append(MENU_PRINT,"Печать","Печать графика")
        f0.AppendSeparator()
        f0.Append(MENU_EXIT,"Выход", "Выход")
        menuBar.Append(f0, "Файл")
        
        # Меню 'Итоговый отчет'
        f1 = wx.Menu()
        f1.Append(MENU_REPORT, "Таблица расчетных параметров")
        f1.AppendSeparator()
        f1.Append(MENU_FILE_REPORT, "Открыть шаблон отчета", "открываем файл итогового отчета")
        menuBar.Append(f1, "Результаты расчета")
        
        # Меню 'Помощь'
        f2 = wx.Menu()
        f2.Append(MENU_HELP, "Краткий справочник", "Краткий справочник")         
        menuBar.Append(f2, "Помощь")
  
        self.SetMenuBar(menuBar)
  
        self.Bind(wx.EVT_MENU, self.onPrint,          id=MENU_PRINT)
        self.Bind(wx.EVT_MENU, self.onPrinterSetup,   id=MENU_PSETUP)
        self.Bind(wx.EVT_MENU, self.onPrinterPreview, id=MENU_PREVIEW)
        self.Bind(wx.EVT_MENU, self.onClipboard,      id=MENU_CLIPB)
        self.Bind(wx.EVT_MENU, self.onExport,         id=MENU_SAVE)
        self.Bind(wx.EVT_MENU, self.onExit ,          id=MENU_EXIT)
        self.Bind(wx.EVT_MENU, self.onFinalReport,    id=MENU_REPORT)
        self.Bind(wx.EVT_MENU, self.OpenFileReport,   id=MENU_FILE_REPORT)
        self.Bind(wx.EVT_MENU, self.onHelp,           id=MENU_HELP)
#------------------------------------------------------------------------------------------------------------
        
        # инициализация данных для печати и установка величин по умолчанию 
        self.pdata = wx.PrintData()
        self.pdata.SetPaperId(wx.PAPER_LEGAL)
        self.pdata.SetOrientation(wx.LANDSCAPE)
        self.margins = (wx.Point(1,15), wx.Point(1,15))
#-------------------------------------------------------------------------------------------------------------------        

    def onFinalReport(self, event):
        
        """открываем таблицу с параметрами """
        
        frame = FinalReportGrid()
        frame.Show()        
#----------------------------------------------------------------------------------------------------------------------
    def OpenFileReport(self, event):
        
        """ открываем итоговый файл отчета """
        
        # выводим сообщение что все удачно
        wx.MessageBox("Вместо этого окна здесь будет открыт файл с итоговым отчетом", "Сообщение", style=wx.OK | wx.ICON_INFORMATION)
#------------------------------------------------------------------------------------------
    # 
    def onPrinterSetup(self, bmp):
        
        """ настройка печати """
        
        data = wx.PageSetupDialogData(self.print_data)

        # Make a copy of our print data for the setup dialog
        dlg_data = wx.PageSetupDialogData(self.print_data)
        print_dlg = wx.PageSetupDialog(self, dlg_data)
        if print_dlg.ShowModal() == wx.ID_OK:
            # Update the printer data with the changes from
            # the setup dialog.
            newdata = dlg_data.GetPrintData()
            self.print_data = wx.PrintData(newdata)
            paperid = dlg_data.GetPaperId()
            self.print_data.SetPaperId(paperid)
        print_dlg.Destroy()

#------------------------------------------------------------------------------------------  
    def onPrinterPreview(self, bmp):
        
        """ предварительный просмотр графика """
        
        printout = self.CreatePrintout(bmp)
        printout2 = self.CreatePrintout(bmp)
        preview = wx.PrintPreview(printout, printout2, self.print_data)
        preview.SetZoom(100)
        if preview.IsOk():
            pre_frame = wx.PreviewFrame(preview, self.parent, "Print Preview")
            # The default size of the preview frame
            # sometimes needs some help.
            dsize = wx.GetDisplaySize()
            width = self.parent.GetSize()[0]
            height = dsize.GetHeight() - 100
            pre_frame.SetInitialSize((width, height))
            pre_frame.Initialize()
            pre_frame.Show()
        else:
            # Error
            wx.MessageBox("Невозможно создать предварительный просмотр", "Ошибка печати", style=wx.ICON_ERROR|wx.OK)        
#------------------------------------------------------------------------------------------------------------  
    def onPrint(self, event):
       
        """ печать графика """
        
        pd = wx.PrintData()

        pd.SetPrinterName("")
        pd.SetOrientation(wx.PORTRAIT)
        pd.SetPaperId(wx.PAPER_A4)
        pd.SetQuality(wx.PRINT_QUALITY_DRAFT)
        # Black and white printing if False.
        pd.SetColour(True)
        pd.SetNoCopies(1)
        pd.SetCollate(True)

        #------------

        pdd = wx.PrintDialogData()

        pdd.SetPrintData(pd)
        pdd.SetMinPage(1)
        pdd.SetMaxPage(1)
        pdd.SetFromPage(1)
        pdd.SetToPage(1)
        pdd.SetPrintToFile(False)
        
        #------------

        dlg = wx.PrintDialog(self, pdd)

        if dlg.ShowModal() == wx.ID_OK:
            dc = dlg.GetPrintDC()

#             dc.StartDoc("My document title")
            dc.StartPage()

            # (wx.MM_METRIC) ---> Each logical unit is 1 mm.
            # (wx.MM_POINTS) ---> Each logical unit is a "printer point" i.e.
#             dc.SetMapMode(wx.MM_POINTS)

#             dc.SetTextForeground("black")
#             dc.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD))
            dc.DrawBitmap(self.bmp, 100, 100)

            dc.EndPage()
#             dc.EndDoc()
            del dc

        else :
            dlg.Destroy()
            
#------------------------------------------------------------------------------------------------------------
    def onClipboard(self, event):
        
        """ копирование в буфер обмена """
        
        # Сделать скриншот всей зоны DC (контекста устройства)
        screen = wx.ScreenDC()
        
        size = screen.GetSize()
        
        # Создать битмап, в котором сохранится скриншот
        bmp = wx.EmptyBitmap(size[0], size[1])
        
        # Создать в памяти DC, который будет использован непосредственно для скриншота
        mem = wx.MemoryDC(bmp)
        
        #Blit в данном случае скопируйте сам экран в кэш памяти
        # и, таким образом, он попадёт в битмап
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        
        del mem  # Release bitmap
        
        # сохраняем скриншот в файл
        bmp.SaveFile('Data\Temporary\screenshot.png', wx.BITMAP_TYPE_PNG)
        
        # выводим сообщение что все удачно
        wx.MessageBox("График успешно сохранен!", "Сообщение", style=wx.OK | wx.ICON_INFORMATION)  
    
#-------------------------------------------------------------------------------------------------------------
    def onKeyEvent(self, event=None):
        
        """ отслеживаем нажатие """
        
        if event == None: 
            return
        
        key = event.GetKeyCode()
        
        if (key < wx.WXK_SPACE or  key > 255):
            return
  
        if (event.ControlDown() and chr(key)=='C'): # Ctrl-C
            self.onClipboard(self)            
#------------------------------------------------------------------------------------------
    def onHelp(self, event=None):
        
        """ вызываем справку """
        
        dlg = wx.MessageDialog(self, self.help_msg, "Краткий справочник", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy() 
#------------------------------------------------------------------------------------------  
    def onExport(self,event=None):
        
        """ сохраняем изображение в файл """
        
        file_choices = "JPG (*.jpg)|*.jpg|" \
                       "PNG (*.png)|*.png|" \
                       "PS (*.ps)|*.ps|" \
                       "EPS (*.eps)|*.eps|" \
                       "BMP (*.bmp)|*.bmp"
  
        thisdir  = os.getcwd()
  
        dlg = wx.FileDialog(self, message='Сохранение изображения',
                            defaultDir = thisdir, defaultFile='Data\Temporary\export_plot.jpg',
                            wildcard=file_choices, style=wx.FD_SAVE)
  
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=300)
            
            if (path.find(thisdir) ==  0):
                path = path[len(thisdir) + 1:]       
#---------------------------------------------------------------------------------------  
    def onExit(self,event=None):
        
        """ выход из окна с графиком """
        
        self.Destroy()        
#---------------------------------------------------------------------------------------  
    def Plot_Data(self):
        
        """ строим график """ 

# считываем значения параметров из файла

        # задаем путь 
        filename = "Data\Termogramma.txt"
        filename1 = "Data\T_par.txt"
        filename2 = "Data\T_neft_bez_ob_nom_d.txt"
        filename3 = "Data\T_neft_nom_d.txt"
        filename4 = "Data\T_jil_nom_d.txt"
        

        # считываем значения
        y = loadtxt(filename, delimiter = " ", unpack=False)
        y1 = loadtxt(filename1, delimiter = " ", unpack=False)
        y2 = loadtxt(filename2, delimiter = " ", unpack=False)
        y3 = loadtxt(filename3, delimiter = " ", unpack=False)
        y4 = loadtxt(filename4, delimiter = " ", unpack=False)

        # Положение осей на графике
        self.axes.xaxis.tick_top()
        self.axes.invert_yaxis()

        # Строим графики
        self.axes.plot(y, x)  # геотерма
        self.axes.plot(y1, x) # парафины
        self.axes.plot(y2, x) # дебит
        self.axes.plot(y3, x) # температура жилы
        self.axes.plot(y4, x) # температура нефти

        # вид разметки осей
        ml_y = MultipleLocator(100) # ось ординат 
        ml_x = MultipleLocator(1) # ось абсцисс

        # рисуем разметку осей (абсцисс и ординат)
        self.axes.xaxis.set_minor_locator(ml_x)
        self.axes.xaxis.set_tick_params(which='minor', right = 'on')

        self.axes.yaxis.set_minor_locator(ml_y)
        self.axes.yaxis.set_tick_params(which='minor', right = 'off')


        # задаем пределы значений по осям
        self.axes.set_xlim(-20, 100) # ось X
        self.axes.set_ylim(3200, 0) # ось Y

        # выводим надписи под осями
        self.axes.set_ylabel(u'Глубина скважины, м')
        self.axes.set_xlabel(u'Температура, C')

        # Рисуем легенду
        self.axes.legend([u'геотерма', u'парафины', u'ном. дебит', u'температура нефти', u'температура жилы'], fontsize = 'medium')

        # Рисуем сетку на графике
        self.axes.grid(True)

############################################################################################################################
class FinalReportGrid(wx.Frame):
    
    """ создаем таблицу параметров """
    
#------------------------------------------------------------------------------------------------------------------------ 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Параметры системы электрообогрева после прогрева скважины ", size=(580, 350))
        
        # Добавляем панель 
        panel = wx.Panel(self, wx.ID_ANY)
        grid = gridlib.Grid(panel)
    
        # задаем количество строк и колонок
        grid.CreateGrid(13, 2)
 
        # задаем названия первого и второго столбца таблицы
        
        grid.SetColLabelValue(0, "Название параметра")
        grid.SetColLabelValue(1, "Значение")

    # записываем значения во второй столбец
        grid.SetCellValue(0, 1, "1 шт.")
        grid.SetCellAlignment(0, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(1, 1, "1625")
        grid.SetCellAlignment(1, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)    
    
        grid.SetCellValue(2, 1, "2")
        grid.SetCellAlignment(2, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(3, 1, "20")
        grid.SetCellAlignment(3, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(4, 1, "680")
        grid.SetCellAlignment(4, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(5, 1, "211")
        grid.SetCellAlignment(5, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(6, 1, "450")
        grid.SetCellAlignment(6, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(7, 1, "119.1")
        grid.SetCellAlignment(7, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(8, 1, "1050")
        grid.SetCellAlignment(8, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(9, 1, "85.7")
        grid.SetCellAlignment(9, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(10, 1, "143.6")
        grid.SetCellAlignment(10, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(11, 1, "42.5")
        grid.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetCellValue(12, 1, "172")
        grid.SetCellAlignment(12, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
 
    # задаем названия параметров по строкам 
        grid.SetCellValue(0, 0, u"Stream Tracer 1.0/50-35/50-1120-480-25")
        grid.AutoSizeColumn(0, setAsMin=True)
        
        grid.SetCellValue(1, 0, u"Длина, м")
        grid.SetCellAlignment(1, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
    
        grid.SetCellValue(2, 0, u"Количество зон разной мощности обогрева")
        grid.SetCellAlignment(2, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(3, 0, u"Длина надземного участка, м")
        grid.SetCellAlignment(3, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(4, 0, u"Питающее напряжение, В")
        grid.SetCellAlignment(4, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(5, 0, u"Ток, А")
        grid.SetCellAlignment(5, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(6, 0, u"Длина горячей (верхней) зоны кабеля, м")
        grid.SetCellAlignment(6, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(7, 0, u"Линейная мощность горячей зоны, Вт/м")
        grid.SetCellAlignment(7, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
                
        grid.SetCellValue(8, 0, u"Длина участка пониженной мощности, м ")
        grid.SetCellAlignment(8, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(9, 0, u"Линейная мощность холодной зоны, Вт/м")
        grid.SetCellAlignment(9, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(10, 0, u"Полная мощность, кВт")
        grid.SetCellAlignment(10, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(11, 0, u"Устьевая температура жидкости не менее, °С")
        grid.SetCellAlignment(11, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        
        grid.SetCellValue(12, 0, u"Максимальная температура внутри кабеля, °С")
     
        grid.SetCellAlignment(12, 0, wx.ALIGN_LEFT, wx.ALIGN_LEFT)        
        
        grid.EnableDragRowSize(True)
        grid.EnableDragColSize(True)
        grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)           
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND, 5)
        panel.SetSizer(sizer)   
        
##################################################################################################  
#--------------------------------------- 'Печать отчета' ----------------------------------------#
##################################################################################################
# Устанавливаем размер шрифта
FONTSIZE = 11

#################################################################################
class TextDocPrintout(wx.Printout):
    """
    Печатаем документ.
    
    Does not handle page numbers or titles, and it assumes that no
    lines are longer than what will fit within the page width.  
    
    """
#-------------------------------------------------------------------------
    def __init__(self, text, title, margins):
        wx.Printout.__init__(self, title)
        self.lines = text.split('\n')
        self.margins = margins

#-------------------------------------------------------------------------
    def HasPage(self, page):
        return page <= self.numPages
    
#-------------------------------------------------------------------------
    def GetPageInfo(self):
        return (1, self.numPages, 1, self.numPages)

#--------------------------------------------------------------------------
    def CalculateScale(self, dc):
        # Scale the DC such that the printout is roughly the same as
        # the screen scaling.
        ppiPrinterX, ppiPrinterY = self.GetPPIPrinter()
        ppiScreenX, ppiScreenY = self.GetPPIScreen()
        logScale = float(ppiPrinterX)/float(ppiScreenX)

        # Now adjust if the real page size is reduced (such as when
        # drawing on a scaled wx.MemoryDC in the Print Preview.)  If
        # page width == DC width then nothing changes, otherwise we
        # scale down for the DC.
        pw, ph = self.GetPageSizePixels()
        dw, dh = dc.GetSize()
        scale = logScale * float(dw)/float(pw)

        # Set the DC's scale.
        dc.SetUserScale(scale, scale)

        # Find the logical units per millimeter (for calculating the
        # margins)
        self.logUnitsMM = float(ppiPrinterX)/(logScale*25.4)

#---------------------------------------------------------------------------------------
    def CalculateLayout(self, dc):
        # Determine the position of the margins and the
        # page/line height
        topLeft, bottomRight = self.margins
        dw, dh = dc.GetSize()
        self.x1 = topLeft.x * self.logUnitsMM
        self.y1 = topLeft.y * self.logUnitsMM
        self.x2 = dc.DeviceToLogicalXRel(dw) - bottomRight.x * self.logUnitsMM 
        self.y2 = dc.DeviceToLogicalYRel(dh) - bottomRight.y * self.logUnitsMM 

        # use a 1mm buffer around the inside of the box, and a few
        # pixels between each line
        self.pageHeight = self.y2 - self.y1 - 2*self.logUnitsMM
        font = wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        self.lineHeight = dc.GetCharHeight() 
        self.linesPerPage = int(self.pageHeight/self.lineHeight)

#------------------------------------------------------------------------------------------
    def OnPreparePrinting(self):
        # calculate the number of pages
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)
        self.numPages = len(self.lines) / self.linesPerPage
        if len(self.lines) % self.linesPerPage != 0:
            self.numPages += 1

#------------------------------------------------------------------------------------------
    def OnPrintPage(self, page):
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)

        # Рисуем контур страницы в пунктирах
        dc.SetPen(wx.Pen("black", 0))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        self.r = wx.RectPP((self.x1, self.y1), (self.x2, self.y2))
        dc.DrawRectangleRect(self.r)
        dc.SetClippingRect(self.r)

        # Draw the text lines for this page
        line = (page-1) * self.linesPerPage
        x = self.x1 + self.logUnitsMM
        y = self.y1 + self.logUnitsMM
        while line < (page * self.linesPerPage):
            dc.DrawText(self.lines[line], x, y)
            y += self.lineHeight
            line += 1
            if line >= len(self.lines):
                break
        return True

######################################################################################################
class PrintFrameworkSample(wx.Frame):
#--------------------------------------------------------------------------------------------    
    def __init__(self):
        wx.Frame.__init__(self, None, size=(900, 800), title="Печать отчета")
        
        # Создаем строку состояний
        self.CreateStatusBar()

        wildcard = "Text source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
        
        # Создаем окно
        frame = wx.Frame(None, title="Открываем файл", size=(800, 700))
        
        # A text widget to display the doc and let it be edited
        self.tc = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_DONTWRAP)
        
        # Задаем параметры отображаемого шрифта документа
        self.tc.SetFont(wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
        
        # Выбираем текущую рабочую директорию
        self.currentDirectory = os.getcwd()

        # Открываем диалог и выбираем файл        
        dialog = wx.FileDialog(None, message="Открытие документа", defaultDir= self.currentDirectory, 
                            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dialog.ShowModal() == wx.ID_OK:
            # This returns the file that was selected
            path = dialog.GetPath()

        # Open the file as read-only and slurp its content
            fileopen = open(path, 'r')
            self.tc.SetValue(fileopen.read())
            fileopen.close()  
     
        self.tc.Bind(wx.EVT_SET_FOCUS, self.OnClearSelection)
        wx.CallAfter(self.tc.SetInsertionPoint, 0)

        # Создаем меню и пункты меню
        
        # Создаем пункты меню
        menu = wx.Menu()
        
        # Добавляем пункт 'Настройка страницы'
        item = menu.Append(-1, "Настройка страницы...\tF5",
                           "Установка параметров страницы и пр.")
        
        # При вызове этого пункта переходим в метод настройки страницы
        self.Bind(wx.EVT_MENU, self.OnPageSetup, item)
        
        # Добавляем пункт 'Настройка печати'
        item = menu.Append(-1, "Настройка печати...\tF6",
                           "Установка настроек принтера и т.д.")
        
        # Добавляем разделитель
        menu.AppendSeparator()
        
        self.Bind(wx.EVT_MENU, self.OnPrintSetup, item)
        
        # Добавляем пункт 'Предварительный просмотр'
        item = menu.Append(-1, "Предварительный просмотр...\tF7",
                           "View the printout on-screen")
        
        self.Bind(wx.EVT_MENU, self.OnPrintPreview, item)
        
        # Добавляем пункт 'Печать'
        item = menu.Append(-1, "Печать...\tF8", "Печать документа")
        
        self.Bind(wx.EVT_MENU, self.OnPrint, item)
        
        # Создаем меню
        menubar = wx.MenuBar()
        
        filemenu = wx.Menu()
        
        quit =filemenu.Append(-1, "Выход", "Выйти из приложения")
        
        # Выходим из программы
        self.Bind(wx.EVT_MENU, self.OnExit, quit)
        
        # Создаем меню 'Файл'
        menubar.Append(filemenu, "&Файл")

        # Создаем пункт меню 'Настройки'
        menubar.Append(menu, "&Настройки")
        
        self.SetMenuBar(menubar)
        
        # Инициализируем данные печати и устанавливаем ряд параметров по умолчанию
        
        self.pdata = wx.PrintData()
        
        # Задаем размер бумаги
        self.pdata.SetPaperId(wx.PAPER_LETTER)
        
        # Задаем ориентацию полей
        self.pdata.SetOrientation(wx.PORTRAIT)
        
        # Устанавливаем отступы полей
        self.margins = (wx.Point(15,15), wx.Point(15,15))

#-------------------------------------------------------------------------------------
# Выходим из редактора

    def OnExit(self, evt):
        self.Close()

#--------------------------------------------------------------------------------------
    def OnClearSelection(self, evt):
        evt.Skip()
        wx.CallAfter(self.tc.SetInsertionPoint, self.tc.GetInsertionPoint())

#--------------------------------------------------------------------------------------
# Настраиваем страницу

    def OnPageSetup(self, evt):
        data = wx.PageSetupDialogData()
        data.SetPrintData(self.pdata)

        data.SetDefaultMinMargins(True)
        data.SetMarginTopLeft(self.margins[0])
        data.SetMarginBottomRight(self.margins[1])

        dlg = wx.PageSetupDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPageSetupData()
            self.pdata = wx.PrintData(data.GetPrintData()) # force a copy
            self.pdata.SetPaperId(data.GetPaperId())
            self.margins = (data.GetMarginTopLeft(), data.GetMarginBottomRight())
        dlg.Destroy()

#------------------------------------------------------------------------------------------------
    def OnPrintSetup(self, evt):
        data = wx.PrintDialogData(self.pdata)
        dlg = wx.PrintDialog(self, data)
        dlg.GetPrintDialogData().SetSetupDialog(True)
        dlg.ShowModal()
        data = dlg.GetPrintDialogData()
        self.pdata = wx.PrintData(data.GetPrintData()) # force a copy
        dlg.Destroy()

#-------------------------------------------------------------------------------------------------
# Предварительный просмотр документа

    def OnPrintPreview(self, evt):
        data = wx.PrintDialogData(self.pdata)
        text = self.tc.GetValue() 
        
        printout = TextDocPrintout(text, "название", self.margins)
        printout2 = None
        printout2 = TextDocPrintout(text, "название", self.margins)
        preview = wx.PrintPreview(printout, printout2, data)

        if not preview.Ok():
            wx.MessageBox("Невозможно открыть предварительный просмотр!", "Ошибка", style=wx.ICON_ERROR|wx.OK)
        else:
            # create the preview frame such that it overlays the app frame
            frame = wx.PreviewFrame(preview, self, "Предварительный просмотр", pos=self.GetPosition(), size=self.GetSize())
#             frame = wx.PreviewFrame(preview, self, "Предварительный просмотр",  wx.Point(100, 100), wx.Size(600, 650))

            # размеры
#             dsize = wx.GetDisplaySize()
#             width = self.parent.GetSize()[0]
#             height = dsize.GetHeight() - 100
#             frame.SetInitialSize((width, height))
            frame.Initialize()
            frame.SetPosition(self.GetPosition())
            frame.SetSize(self.GetSize())
            frame.Show()

#--------------------------------------------------------------------------------------------
# Отправляем документ на печать

    def OnPrint(self, evt):
        data = wx.PrintDialogData(self.pdata)
        printer = wx.Printer(data)
        text = self.tc.GetValue() 
        printout = TextDocPrintout(text, "название", self.margins)
        useSetupDialog = True
        
        if not printer.Print(self, printout, useSetupDialog) \
           and printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox(
                "Возникла проблема при печати.\n"
                "Возможно Ваш текущий принтер не настроен корректно?",
                "Ошибка печати", style=wx.ICON_ERROR|wx.OK)
        else:
            data = printer.GetPrintDialogData()        # сохраняем копию данных для печати в будущем
            self.pdata = wx.PrintData(data.GetPrintData()) # принудительное копирование
        printout.Destroy()

##################################################################################################  
#------------------------------------------- 'Помощь' -------------------------------------------#
##################################################################################################

class HelpWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(HelpWindow, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):

        toolbar = self.CreateToolBar()
        toolbar.AddTool(1, 'Выход', wx.Bitmap('Picture\Texit.png'))
        toolbar.AddTool(2, 'Помощь', wx.Bitmap('Picture\Help.png'))
        
        toolbar.Realize()

        self.splitter = wx.SplitterWindow(self)
        
        self.panelLeft = wx.Panel(self.splitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)

        self.panelRight = wx.Panel(self.splitter)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        header = wx.Panel(self.panelRight, wx.ID_ANY)

        header.SetBackgroundColour('#6f6a59')
        header.SetForegroundColour('white')
        
        # Размещаем картинку
        icon = wx.Icon('Picture\Help icon.png', wx.BITMAP_TYPE_PNG)
        # Показываем в окне
        self.SetIcon(icon)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        st = wx.StaticText(header, wx.ID_ANY, 'Помощь')
        font = st.GetFont()
        font.SetFamily(wx.FONTFAMILY_ROMAN)
        font.SetPointSize(11)
        st.SetFont(font)

        hbox.Add(st, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 8)

        closeBtn = wx.BitmapButton(header, wx.ID_ANY, wx.Bitmap('Picture\Close.png', wx.BITMAP_TYPE_PNG), style=wx.NO_BORDER)
        
        closeBtn.SetBackgroundColour('#6f6a59')
        
        hbox.Add(closeBtn, 0, wx.TOP|wx.BOTTOM, 8)
        header.SetSizer(hbox)

        vbox2.Add(header, 0, wx.EXPAND)

        helpWin = html.HtmlWindow(self.panelRight, style=wx.NO_BORDER)
        
        helpWin.LoadPage('html\help.html')

        vbox2.Add(helpWin, 1, wx.EXPAND)

        self.panelRight.SetSizer(vbox2)
        self.panelLeft.SetFocus()

        self.splitter.SplitVertically(self.panelLeft, self.panelRight)
        self.splitter.Unsplit()

        self.Bind(wx.EVT_BUTTON, self.CloseHelp, id=closeBtn.GetId())
        self.Bind(wx.EVT_TOOL, self.OnCloseHelp, id=1)
        self.Bind(wx.EVT_TOOL, self.OnHelp, id=2)

        self.panelLeft.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.panelLeft.SetFocus()

        self.CreateStatusBar()

        self.SetTitle('Помощь')
        self.Centre()

    def OnCloseHelp(self, e): 
        self.Close()
        
    def OnHelp(self, e):
        self.splitter.SplitVertically(self.panelLeft, self.panelRight, 0)
        self.panelLeft.SetFocus()

    def CloseHelp(self, e):

        self.splitter.Unsplit()
        self.panelLeft.SetFocus()

    def OnKeyPressed(self, e):

        keycode = e.GetKeyCode()
        print(keycode)

        if keycode == wx.WXK_F1:

            self.splitter.SplitVertically(self.panelLeft, self.panelRight, 0)
            self.panelLeft.SetFocus()
            
# end = time.time()   
# end-start
####################################################################################################
# Главный цикл
if __name__ == '__main__':
    main()