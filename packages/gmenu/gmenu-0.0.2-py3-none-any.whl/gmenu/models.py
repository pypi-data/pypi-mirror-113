from django.db import models
from django.contrib.auth.models import User

class menu_kinds(models.TextChoices):
    '''
        Jenis menu : 
            0 : Front end without user login
            1 : Front end with user login
            2 : Back end with user login (nothing for none user)
    '''
    FRONTEND_UNLOGIN = 'frontend_unlogin'
    FRONTEND_LOGIN = 'frontend_login'
    BACKEND_LOGIN = 'backend_login'
    
class menu(models.Model):
    '''
        # Buat relasi one to one terhadap menu
        # sesuai kebutuhan :
        #   di sarankan ke site, atau user
        #   user = models.ManyToManyField(User)
        #   site = models.ManyToManyField(Site)
        #   
        #   Jika menggunakan site, didalam site ada user, maka lebih baik lagi
        #   create menu berdasarkan user
        #   Final : menggunakan user (generate menu berdasarkan user yg login)

        Dasar menu diambil dari user : admin
        jika ada penambahan user, otomatis copy juga menu yg sama seperti menu admin
            selanjutnya user bisa berkreasi sendiri

        DO_NOTHING tidak disarankan digunakan, sebaiknya gunakan protect
        untuk membatasi jika user melakukan penghapusan data
    '''

    # user: untuk filter berdasarkan user yang login
    user = models.ManyToManyField(User) 

    # parent: untuk membuat struktur menu    
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)   

    # name: nama menu
    name = models.CharField(max_length=100)
    
    # link: adalah nama menu yg di slugify
    # href di ubah menjadi link
    # jika ada ://www maka dianggap link luar
    link = models.CharField(max_length=255, null=True, blank=True)       

    # icon: jika menggunakan link awesome font
    icon = models.CharField(max_length=50, null=True, blank=True)

    # order_menu: untuk menentukan urutan menu
    order_menu = models.IntegerField(default=0)

    # is_admin_menu: jika true, menu untuk backend, jika false menu untuk frontend
    # jenis menu
    kinds = models.CharField(max_length=20, choices=menu_kinds.choices, default=menu_kinds.FRONTEND_UNLOGIN)

    # is_visibled: untuk menyembunyikan menu
    is_visibled = models.BooleanField(default=True)	
    
    # is_master_menu: adalah menu yg digunakan oleh banyak user
    # tidak bisa dihapus, hanya super user yg bisa menghapus
    # is_master_menu adalah menu yg di copy oleh user lain saat pertama kali di buat
    is_master_menu = models.BooleanField(default=False)	

    # is_statis_menu: penanda halaman statis
    # semua menu yg di create oleh user adalah statis menu
    # diakses khusus melalui link tertentu di halaman statis
    is_statis_menu = models.BooleanField(default=False)	

    # created_at tanggal create
    created_at = models.DateTimeField(auto_now_add=True)

    # update_at tanggal update
    updated_at = models.DateTimeField(auto_now=True) 

    # tampilan menu saat berada di lookup dan halaman admin (khusus halaman admin jika tidak ada display_list)
    def __str__(self):          
        if self.kinds == menu_kinds.FRONTEND_UNLOGIN or self.kinds == menu_kinds.FRONTEND_LOGIN:
            res = '[ Front End ]'       # halaman depan
        else:
            res = '[ Back End ]'       # halaman dashboard

        if self.parent:
            par = self.parent.name      # tampilkan nama parent jika ada    
        else:
            par = ''

        return "{} {} > {}".format(res, par, self.name)        

    # menentukan order data saat di tampilkan di halaman frontend maupun backend
    #class Meta:
    #    ordering = ['kinds','parent_id','order_menu']

    # slugify menu link dilakukan di form
    # karena ada menu link yg di kosongkan