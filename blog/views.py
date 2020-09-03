from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Post
from .models import SyainTable
from .models import KojinTourokuTable
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_list_or_404
from .forms import PostForm
from .forms import SyainForm
from .forms import MustWokerlineFormSet
from django.contrib.auth.decorators import login_required
import pdb #まずpdbをインポート
import urllib.request, json #google map api
import urllib.parse  #google map api
import datetime  #google map api



# Create your views here.
#posts = Post.objects.filter(title__contains='title')
#posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

def post_list(request):
  #posts = Post.objects.filter(title__contains='title')
  posts = Post.objects.all()
  return render(request, 'blog/post_list.html', {'posts': posts})

def post_list_Serch(request,id):
   #posts = Post.objects.all()
  if id==0:#未完了分を表示　ここの分岐が上手くできていない　とりだしたデータのカズもあっていない⇒解決
      posts = Post.objects.filter(compleat_date__isnull=True)
  else:#期限超過分を表示　⇒うまくとりだせない ⇒右辺が上手くいっていない？？
      dt_now4 =datetime.datetime.today()#これは情報を取り出せている
      dt_now1 =datetime.datetime.now()#これは情報を取り出せている
      dt_now2 =datetime.datetime.now#これはポインタのようなものが取り出されるだけ
      dt_now3 =datetime.datetime.today#これはポインタのようなものが取り出されるだけ
      #条件としては　完了していなくて　期限を超過していないものを抽出する（and検索）
      posts = Post.objects.filter(compleat_date__isnull=True,fixed_date__lte=datetime.datetime.today().date())
      #posts = Post.objects.filter(fixed_date__lte=datetime.datetime.today().date())#これは落ちないが検索結果も正しそう
      #posts = Post.objects.filter(fixed_date__lte=datetime.datetime.today().date)#これは落ちる

      #posts = Post.objects.filter(fixed_date__lte=datetime.datetime.now)#datetimeは怒られない おなじくTypeError at /post_list_Serch/1/ expected string or bytes-like object
      #posts = Post.objects.filter(fixed_date__lte=datetime.datetime.today)#datetimeは怒られない TypeError at /post_list_Serch/1/ expected string or bytes-like object
      #posts = Post.objects.filter(fixed_date__lte=datetime.today())#todayという属性はないと言われる
      #posts = Post.objects.filter(fixed_date__lte=date.today())#dateが定義されていないと言われる
      #posts = Post.objects.filter(fixed_date__lte=today)#todayが定義されていないと言われる

      #posts = Post.objects.filter(fixed_date__date=datetime.datetime.now().date)
  return render(request, 'blog/post_list.html', {'posts': posts})
   #posts = Post.objects.filter(fixed_date__isnull=True)
   #posts = Post.objects.filter(fixed_date__year=2019)#これだと該当のデータを取り出せる
   #datetimeフィールドであることが関連するのでは
   #posts = Post.objects.filter(fixed_date__datetime=datetime.datetime.now()) DateTimeFieldのサポートされていないルックアップ 'datetime'または許可されていないフィールドでの結合、おそらく時間または日付を意味しますか？
   #posts = Post.objects.filter(compleat_date > timezone.today())#todayもnowも()をつけてもだめ
   #posts = Post.objects.filter(fixed_date__isnull=True)


def post_detail(request, pk):

    class DispData:
        def __init__(self):
            '''self.author = 0 #ひとまずコメントにしておく
            self.title = 'abc'
            self.title2 = 'abc'
            self.text = 'abc'
            self.created_date = 0
            self.published_date = 0
            self.fixed_date = 0
            self.compleat_date = 0
            self.kanren_member = 0
            self.pk = 0'''
            #初期値は入れない　いれると　HTMLに渡したときに初期値で上書きされてしまうので
            self.author
            self.title
            self.title2
            self.text
            self.created_date
            self.published_date
            self.fixed_date
            self.compleat_date
            self.kanren_member
            self.pk

    dispData = DispData
    post = get_object_or_404(Post, pk=pk)

    dispData.author = post.author
    dispData.title = post.title
    dispData.title2 = post.title2
    dispData.text = post.text
    dispData.created_date = post.created_date
    dispData.published_date = post.published_date
    dispData.fixed_date = post.fixed_date
    dispData.compleat_date = post.compleat_date
    dispData.pk = post.pk #これをいれると画面は表示されるようになったけど　どこにpkなんて定義されているのか
    #⇒また、表示が０になってしまうのはなぜか？？　初期値が表示されている。。。⇒初期値をいれなければ正しく表示された
    #クラスをつくってそのなかにデータをいれこんでＨＴＭＬに渡してやればよい

    kojinTourokuTables = get_list_or_404(KojinTourokuTable,KojinTourokuNo=pk)

    nameWork = ''
    #for kojinTourokuTable in kojinTourokuTables:
    for i, kojinTourokuTable in enumerate(kojinTourokuTables,0): #iにインデックスが格納される　第２引数はインデックスの初期値
        if i != 0:
            nameWork += ','
        syainname = get_object_or_404(SyainTable,SyainNo=kojinTourokuTable.SyainNo)#社員名を取得できている
        nameWork += syainname.name

    dispData.kanren_member = nameWork

    #追加処理
    form = PostForm(request.POST)#ここの戻ってきたところで関連のデータをいれてやればよいのではないか
    context = {'form': form}
    context['dispData'] = dispData
    must_workers = post.must_worker.all()#追加しました　20200818
    context['must_workers']=must_workers
    #return render(request, 'blog/post_detail.html', {'dispData': dispData},{'must_workers': must_workers})#なんか質問ウィンドウがでる

    #return render(request, 'blog/post_detail.html', {'post': post})#html側に関係者を渡したいのだがどうやるのか⇒表示用のモデルをつくるか？⇒構造体つくって渡せばよいのでは？
    #★動くやつ return render(request, 'blog/post_detail.html', {'dispData': dispData})#html側に関係者を渡したいのだがどうやるのか⇒構造体つくって渡せばよいのでは？★これが動くもの
    return render(request, 'blog/post_detail.html', context)
    #上記を呼んだあとどこかで例外が発生する　今のところ　html側で参照しているメンバをすべてよういしてないことが原因かと思われる
    #⇒全部入れ込んでみたが同じだった　何が悪いのか？　post.pk がないと言われているようにみえるが　どこに定義されているのか
    #オブジェクトの値を引き継ぐようにできないか(DBにする必要がある？）
@login_required
def post_new(request):
    #must_workers = post.must_worker.all()#追加しました　20200818　この操作は入力がされた後のもの　入力はどうやるのか
    form = PostForm(request.POST)#ここの戻ってきたところで関連のデータをいれてやればよいのではないか
    context = {'form': form}
    if request.method == "POST":
        #form = PostForm(request.POST)#ここの戻ってきたところで関連のデータをいれてやればよいのではないか
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:#get の場合
        # 空のformsetをテンプレートへ渡す
        context['formset'] = MustWokerlineFormSet()
        #form = PostForm()
        #return render(request, 'blog/post_edit.html', {'form': form})#ここからもワーカーを渡すべきでは
        #return render(request, 'blog/post_edit.html', {'form': form, 'must_workers':must_workers})#変更20200818

    return render(request, 'blog/post_edit.html', context)#ここからもワーカーを渡すべきでは
''' # ここは仮作成なのでコメントにしています
@login_required
def post_edit(request, pk):
    #post = get_object_or_404(Post, pk=pk)
    #kojinTourokuTables = KojinTourokuTable.objects.all()#これはうごいているのでしょう

    #以下で取得できた　以下は1件取得することができるのでループさせるとよい　get_list_or_404　でとるとよい　とったものは配列風に参照できる   
    #kojinTourokuTables = get_object_or_404(KojinTourokuTable,KojinTourokuNo=pk)#Postのid とKojinTourokuTableのKojinTourokuNoが一致するものを取り出したい
    kojinTourokuTables = get_list_or_404(KojinTourokuTable,KojinTourokuNo=pk)

    nameWork = ''
    #for kojinTourokuTable in kojinTourokuTables:
    for i, kojinTourokuTable in enumerate(kojinTourokuTables,0): #iにインデックスが格納される　第２引数はインデックスの初期値
        if i != 0:
            nameWork += ','
        syainname = get_object_or_404(SyainTable,SyainNo=kojinTourokuTable.SyainNo)#社員名を取得できている
        nameWork += syainname.name

    #ループさせてひとつの文字列エリアに格納それを　Syainnames とする
    #Syainnames　=　kojinTourokuTable.SyainNo　#実行するとこれが即例外になる
    #kojinTourokuTable.objects.filter(KojinTourokuNo=post.id)　#これは動かない
    if request.method == "POST":
        form = SyainForm(Syainname)#引数は何をセットすればよいのだ？？★★
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = SyainForm(initial = {'names': nameWork})
        #form = SyainForm(initial = {'names': syainname.name}) #これだと表示された 
        #form = SyainForm(initial = {'names': syainname})  これだとなにか違うのが表示された　表示はされる
        #form = SyainForm(instance=Syainname.name) #これはモデルフォームのときのやりかたでは？
        #form = SyainForm() #これだと空のフォームが表示されます
     
    return render(request, 'blog/post_edit.html', {'form': form})
'''    
@login_required
def post_edit(request, pk):
    form = PostForm(request.POST)#追加しました　20200818
    context = {'form': form}#追加しました　20200818
    post = get_object_or_404(Post, pk=pk)
    must_workers = post.must_worker.all()#追加しました　20200818
    if request.method == "POST":#html からpostされたときに通すルート

        form = PostForm(request.POST, instance=post)
        formset = MustWokerlineFormSet(request.POST, instance=post)#追加しました　20200818
        if form.is_valid():#ここで選択されたリストをDBに反映したい
            listret = request.POST.getlist("sample22")

            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            formset.save()#追加しました　20200818 ★ここでおちることもある
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {'form': form}#追加しました　20200818
        context['formset'] = MustWokerlineFormSet(instance=post) #表示はされたけど空っぽのものが表示された⇒なぜだ、POSTにも値が入っている⇒フォームに値をいれていないから
        context['must_workers'] = must_workers
        context['must_workers_count'] = must_workers.count()
        #formset = MustWokerlineFormSet(instance=post)
    return render(request, 'blog/post_edit.html', context)#変更20200818　★正しく表示されるもの
    #return render(request, 'blog/post_edit.html', {'form': form},{'formset': formset}) #これだと変な表示がでる
    #return render(request, 'blog/post_edit.html', {'form': form},{'formset': formset},{'must_workers': must_workers})#例外になる
    #return render(request, 'blog/post_edit.html', {'form': form})    #変更まえ
    #return render(request, 'blog/post_edit.html', {'form': form,'pk':pk})#引数は複数渡すことができるみたいです

@login_required
def post_memberset(request, pk):
    #post = get_object_or_404(Post, pk=pk)
    #kojinTourokuTables = KojinTourokuTable.objects.all()#これはうごいているのでしょう

    #以下で取得できた　以下は1件取得することができるのでループさせるとよい　get_list_or_404　でとるとよい　とったものは配列風に参照できる   
    #kojinTourokuTables = get_object_or_404(KojinTourokuTable,KojinTourokuNo=pk)#Postのid とKojinTourokuTableのKojinTourokuNoが一致するものを取り出したい
    kojinTourokuTables = get_list_or_404(KojinTourokuTable,KojinTourokuNo=pk)

    nameWork = ''
    #for kojinTourokuTable in kojinTourokuTables:
    for i, kojinTourokuTable in enumerate(kojinTourokuTables,0): #iにインデックスが格納される　第２引数はインデックスの初期値
        if i != 0:
            nameWork += ','
        syainname = get_object_or_404(SyainTable,SyainNo=kojinTourokuTable.SyainNo)#社員名を取得できている
        nameWork += syainname.name

    #ループさせてひとつの文字列エリアに格納それを　Syainnames とする
    #Syainnames　=　kojinTourokuTable.SyainNo　#実行するとこれが即例外になる
    #kojinTourokuTable.objects.filter(KojinTourokuNo=post.id)　#これは動かない
    if request.method == "POST":
        form = SyainForm(Syainname)#引数は何をセットすればよいのだ？？★★
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = SyainForm(initial = {'names': nameWork})
        #form = SyainForm(initial = {'names': syainname.name}) #これだと表示された 
        #form = SyainForm(initial = {'names': syainname})  これだとなにか違うのが表示された　表示はされる
        #form = SyainForm(instance=Syainname.name) #これはモデルフォームのときのやりかたでは？
        #form = SyainForm() #これだと空のフォームが表示されます
        #git用についか
    return render(request, 'blog/post_memberset.html', {'form': form})
    
