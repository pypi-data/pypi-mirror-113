'''
    Generate menus - create by ione
    Class ini untuk generate menu sesuai dengan data di database
    Date 13-02-21

    Update v2.0:
        # Sdh mengikuti update terakhir dari project OPD
        # Atur ulang tab
        # Ikuti model tabel menu yg ada di project ini atau OPD

    Update v2.1:
        # create menu berdasarkan user yg login
        # untuk front end, karena tidak login maka generate menu berdasarkan
        # user yg berada di site tersebut
'''

# Tambah dictionary sesuai data di database, Algoritma :
# 1. Buat query Order by parent id dan order menu
# 2. copy data ke mDict record per pecord
# 3. Append ke mList, sehingga jadinya list of dictionary
# 4. Atur ulang mList, sehingga urutannya menjadi :
#    Menu Parent
#       |--- Menu Anak1
#       |--- Menu Anak2, dst...
# 5. Atur Ulang Level, sehingga menjadi :
#    Dictionary memiliki item baru
#       1. Level : untuk menentukan kedalaman level menu anak
#       2. HaveChild : True or False, Untuk penanda apakah menu parent mempunyai anak atau tidak
#       3. haveChildEndTag : Type Integer, Untuk penanda tag penutup menu anak di buat
#          Jika level 1, buat satu tag penutup menu anak
#          Jika level 2, buat dua tag penutup menu anak, dst...
# 6. Atur active menu
# Buat function baru untuk Atur BreadCrumb, tambahkan List of Dictionary dengan format 
#       [{'Nama','href'},{'nama2','href2'}]
#       Data ini akan di cek di template dengan cara yang sama seperti generate menu
#  --------------------------------------------------------------------------------------------------          

from . models import menu
from django.db.models import F
import json
from django.http import JsonResponse

# import logging
# logger = logging.getLogger(__name__)

class Menus:      
    mDict = {}     
    mList = []      # result ada di mList

    def __init__(self, key_filter, pKinds, pIs_master_menu = False):         # key_filter adalah filter untuk company tertentu saja
        if len(self.mList) == 0:
                #if key_filter != "":
            self.create_menus(key_filter, pKinds, pIs_master_menu)
        else:
            self.mDict = {}  # clear dulu (karena prosedur init ini sekali dijalankan saat class di buat)
            self.mList = []
            self.create_menus(key_filter, pKinds, pIs_master_menu)                    

    def get_menus(self):
        return self.mList

    # Conver dari string ke List (untuk bread crumbs)
    def convert_StrToList(self, str):
        li = list(str.split(" - "))       # Delimeter " - " agar spasi juga ikut di hilangkan
        return li      

    # misal menu aktif = customer, maka menu customer dan menu data master status aktif
    def find_activeMenuList(self, act_menu):
        mCount = 0
        mList = []      # local variable
        while mCount < len(self.mList):
            if act_menu.lower() == self.mList[mCount]['nama'].lower():
                mList = self.mList[mCount]['activeMenu']
                break
            mCount += 1
        return mList        

    # informasi level tidak bisa dari data sebelumnya
    # harus dihitung dari posisi menu terhadap root parent
    def get_menuLevel(self, key_filter, menu_id):
        #Site.objects.filter(id=siteID).values_list('name',flat=True) # kalau tidak mengandung imageField gunakan cara ini
        id = menu_id
        mlevel = 0
        #mid = menu.objects.get(user__id=key_filter, id=id)

        # pakai get jika tidak ada data menyebabkan error
        mid = menu.objects.filter(user__id=key_filter, id=id).first()
        # Error jika mid kosong 
        # kembalikan kosong
        if mid:
            while mid.parent_id is not None:
                mlevel += 1
                id = mid.parent_id
                mid = menu.objects.filter(user__id=key_filter, id=id).first()
                if not mid: break

        return mlevel

    def create_breadCrumb(self, act_menu):
        # 6. Buat sesuai menu yang aktif saja Bread Crumbs
        # String untuk bread crumb, ini yg akan di convert menjadi list                               
        mDict = {}              # variable local
        mList = []              # variable local
        mListCount = 0
        mCount1 = 0                
        mParentID = 0                
        mNama = ""

        # Masukkan dashboard/home di root dari breadcrumb
        # Jika posisi sudha di dachboard, tidak perlu bisa di klik lagi
        if len(self.mList) > 0:      # Tambahan baris ini dari project django-opd
            mNama = self.mList[0]['nama']
            if mNama.lower() != act_menu.lower():
                mDict[mListCount] = {'id':mListCount, 'nama':mNama, 'href':self.mList[0]['href']}
            else:
                mDict[mListCount] = {'id':mListCount, 'nama':mNama, 'href':'#'}
            mList.append(mDict[mListCount])
            mListCount += 1
            mOrder = 1

        # Jika active menu bukan home atau dashboard
        if mNama.lower() != act_menu.lower():
            # Cari menu yg aktif di list
            while mCount1 < len(self.mList):
                mNama = self.mList[mCount1]['nama']
                if mNama.lower() == act_menu.lower():
                    mParentID = self.mList[mCount1]['parent_id']                                          
                    mDict[mListCount] = {'id':mListCount, 'nama':self.mList[mCount1]['nama'], 'href':'#'} # href di buat '#' karena posisi page aktif adalah customer, jadi tidak perlu di klik lagi
                    mList.append(mDict[mListCount])
                    mListCount += 1
                    break  
                mCount1 += 1 

            # Cari dari posisi menu aktif ke root                                        
            mCount1 = 0
            while mCount1 < len(self.mList): 
                if mParentID is None:                                                                                                                
                    break
                elif mParentID == self.mList[mCount1]['id']:                                        
                    mParentID = self.mList[mCount1]['parent_id']   
                    mDict[mListCount] = {'id':mListCount, 'nama':self.mList[mCount1]['nama'], 'href':self.mList[mCount1]['href']}
                    mList.insert(mOrder,mDict[mListCount])
                    mListCount += 1
                    mOrder += 1
                    mCount1 = 0 # Ulang looping dari awal
                mCount1 += 1  

        return mList    

    def create_menus(self, key_filter, pKinds, pIs_master_menu):     
        # 0. Sebelum proses menu, update dulu seluruh menu yg id = id parent set id parent = NULL untuk menghindari
        # looping tidak terbatas
        menu.objects.filter(id=F('parent_id')).update(parent_id=None)    # query pengaman

        # 1. Buat Query Order By Parent_id dan Order_menu    berita__site_id
        #mData = menu.site.through.objects.filter(menu__site=key_filter)
        #mData = menu.site.through.objects.filter(menu__site=key_filter).order_by('menu__parent_id','menu__order_menu')
        # is_master_menu=pIs_master_menu (gak pakai ini karena, munculin semua menu termasuk yg bukan master menu)    
        # di datatables cuma munculin yg master menu = False
        if pIs_master_menu: # is_visible munculin checkbox, siap untuk di edit
            mData = menu.objects.filter(user__id=key_filter, kinds=pKinds).order_by('parent_id','order_menu')
        else:
            mData = menu.objects.filter(user__id=key_filter, kinds=pKinds, is_visibled=True).order_by('parent_id','order_menu')

        # logger.error(' ----------------------- DATA TABEL MENU -----')
        # logger.error(mData)
        # 2. Copy data dari tabel ke mDict 
        # 3. Hasil langsung append ke mList
        mID = ''
        for m in mData:      
            mID = m.id
            self.mDict[mID] = {'id':mID, 'nama':m.name, 'href':m.link, 'icon':m.icon, 'parent_id':m.parent_id, 'is_visibled':m.is_visibled}
            self.mList.append(self.mDict[mID])

        # 4. Atur ulang urutan mList
        #logger.error(' ----------------------- DATA TABEL MENU 1-----')
        
        mCount1 = 0
        mCount2 = 0
        mOrder  = 0     # Supaya urutan menu anak tidak berubah
        while mCount1 < len(self.mList):
            mCount2 = mCount1 + 1
            mOrder  = 0                        
            while mCount2 < len(self.mList):                                
                if self.mList[mCount1]['id'] == self.mList[mCount2]['parent_id']:
                    mOrder += 1
                    self.mList.insert(mCount1+mOrder, self.mList[mCount2])
                    self.mList.pop(mCount2+1)
                mCount2 += 1
            mCount1 += 1

        #logger.error(' ----------------------- DATA TABEL MENU 2-----')

        # 5. Atur ulang level menu
        #    Tambah item baru di dictionary (HaveChildEndTag) diisi sesuai nilai level
        mCount1 = 0             # reset variabel                            
        mLevel  = 0             # untuk tambah item baru di dictionary (Level)
        mLevel_prev  = 0
                       
        #mIsHaveChild = 0        # untuk tambah item baru di dictionary (HaveChild)                
        while mCount1 < len(self.mList):
            mLevel = self.get_menuLevel(key_filter, self.mList[mCount1]['id'])
            self.mList[mCount1]['level'] = mLevel 

            self.mList[mCount1]['haveChild'] = 0 
            if mCount1 > 0:      # Cek dulu apakah index > 0 karena ada pengecekan List sebelum
                if self.mList[mCount1]['parent_id'] == self.mList[mCount1-1]['id']:
                    self.mList[mCount1-1]['haveChild'] = 1 

            # end tag jika level menurun, maka end tag adalah selisih level sekarang dan sebelum
            self.mList[mCount1]['haveChildEndTag'] = 0
            selisih = mLevel - mLevel_prev
            if selisih < 0:
                self.mList[mCount1-1]['haveChildEndTag'] = -selisih

            mLevel_prev = mLevel

            # mParentID = self.mList[mCount1]['parent_id']                        
            # if mParentID is None:
            #     mLevel = 0
            #     mIsHaveChild = 0                                  
            # elif mCount1 > 0:      # Cek dulu apakah index > 0 karena ada pengecekan List sebelum
            #     if mParentID == self.mList[mCount1-1]['id']:
            #         mLevel += 1
            #         mIsHaveChild = 1
            #     elif mParentID != self.mList[mCount1-1]['parent_id']: 
            #         mLevel -= 1
            #         mIsHaveChild = 0

            # self.mList[mCount1]['level'] = mLevel 
            # self.mList[mCount1]['haveChild'] = 0
            # if mCount1 > 0:                       
            #     self.mList[mCount1-1]['haveChild'] = mIsHaveChild                                           
                

            

            # # update haveChildEndTag
            # self.mList[mCount1]['haveChildEndTag'] = 0
            # if mCount1 > 0:                       
            #         if self.mList[mCount1-1]['level'] > self.mList[mCount1]['level']:
            #                 self.mList[mCount1-1]['haveChildEndTag'] = 1 # self.mList[mCount1-1]['level']

            # # Looping terakhir masih di level > 0
            # if mCount1 == len(self.mList)-1:                                
            #         self.mList[mCount1]['haveChildEndTag'] = 1 # self.mList[mCount1]['level']

            # mIsHaveChild = 0
            mCount1 += 1

        #logger.error(' ----------------------- DATA TABEL MENU 3-----')

        # 6. Atur Active Menu
        # String untuk bread crumb, ini yg akan di convert menjadi list
        mBreadCrumb = ""    # msh ada error (di site dikes) #BUG FOUND
        
        # sementara karena ada error
        # while mCount1 < len(self.mList):
        #     self.mList[mCount1]['activeMenu'] = "" # self.convert_StrToList(mBreadCrumb.lower())
        # Error terjadi karena Ada menu yg parent ID ke diri sendiri
        # recursive error 
        # user input dari halaman admin (halaman ini tidak ada validasi input)
        
        mParentID = 0 
        mCount1 = 0
        mCount2 = 0
        while mCount1 < len(self.mList):
            mParentID = self.mList[mCount1]['parent_id']    
            mCount2 = 0
            mBreadCrumb = ""
            while mCount2 < len(self.mList): 
                if mParentID is None:                                        
                    if mBreadCrumb != "":
                            mBreadCrumb += " - "
                    mBreadCrumb += self.mList[mCount1]['nama']
                    break
                elif mParentID == self.mList[mCount2]['id']:
                    if mBreadCrumb != "":
                            mBreadCrumb += " - "
                    mBreadCrumb += self.mList[mCount2]['nama'] 
                    mParentID = self.mList[mCount2]['parent_id']     
                    mCount2 = 0     # Ulang looping dari awal
                mCount2 += 1                        

            # Update BreadCrumb
            self.mList[mCount1]['activeMenu'] = self.convert_StrToList(mBreadCrumb.lower())
            # mBreadCrumb = "" # Reset Bread Crumb
            mCount1 += 1

        #return self.mList            # result   
        #logger.error(' ----------------------- DATA TABEL MENU 4-----')

    # def find_activeMenuList_json(self, act_menu):
    #     return JsonResponse(self.find_activeMenuList(self, act_menu))

    # def create_breadCrumb_json(self, act_menu):
    #     return JsonResponse(self.create_breadCrumb(self, act_menu))

    # def get_menus_json(self):
    #     return json.dumps(self.mList)
        #return JsonResponse(self.mList)