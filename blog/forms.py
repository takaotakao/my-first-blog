import bootstrap_datepicker_plus as datetimepicker
#import bootstrapDualListbox

from django import forms

from .models import Post,SyainTable
class SyainTableForm(forms.ModelForm):

    class Meta:
        model = SyainTable
        fields = ('name', )
        labels = {
        	'name': '名前',
        }

class PostForm(forms.ModelForm):
    '''
    must_worker = forms.ModelMultipleChoiceField(#これは関係を表す定義で2種類しかない
        
        queryset=SyainTable.objects.all().name,
        #widget=forms.CheckboxSelectMultiple　#デフォルトでよいので指定しない。
    )
    '''
    class Meta:
        model = Post
        fields = ('title','text','title2','fixed_date','compleat_date', 'must_worker',)
        widgets = {
            'fixed_date': datetimepicker.DateTimePickerInput(
                format='%Y-%m-%d %H:%M:%S',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ),
            'compleat_date': datetimepicker.DateTimePickerInput(
                format='%Y-%m-%d %H:%M:%S',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
            ),
            #ここ作成途中ブートストラップを入れ込みたい
            #'must_worker': bootstrapDualListbox(),
            
        }
        labels = {
        	'title': 'Todoタイトル',
        	'text': 'Todo詳細',
        	'title2': '記入者',
        	'fixed_date': '期日',
        	'compleat_date': '完了日',
            'must_worker': '対象者',
        }
        exclude = ('SyainTable',)
        #exclude = ('SyainTableForm',) これをやると例外になる



MustWokerlineFormSet = forms.inlineformset_factory(
    #Post, Post.must_worker.through, fields='__all__', can_delete=False,max_num=3#これは動くやつ
    Post, Post.must_worker.through, fields='__all__', can_delete=False, max_num=1,widgets={'must_worker': forms.SelectMultiple}

    #Post, Post.must_worker.through, fields=('SyainNo',), can_delete=False#これは例外になりました
    #新規の場合はmax_numの個数通りになる　編集の場合は入力されている個数分
    #Post, Post.must_worker.through,  fields=('name','SyainNo'),can_delete=False#これは例外になりました
    #Post, Post.must_worker.through, fields='__all__', can_delete=False,max_num=3,widgets={'details': Textarea(attrs={'cols': 40})
    #Post, Post.must_worker.through, fields=('name'), can_delete=False#これは例外になりました
    #widgets={'name': Textarea(attrs={'cols': 80, 'rows': 20})})
)

#社員テーブルのモデルフォームをつくることで、入力画面のデザインを編集できるのでは

class SyainForm(forms.Form):
    names = forms.CharField(max_length=100)

