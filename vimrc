" setting
"文字コードをUFT-8に設定
set fenc=utf-8
"" バックアップファイルを作らない
"set nobackup
"" スワップファイルを作らない
"set noswapfile
" 編集中のファイルが変更されたら自動で読み直す
set autoread
" バッファが編集中でもその他のファイルを開けるように
set hidden
" 入力中のコマンドをステータスに表示する
set showcmd

" 見た目系
"全体の見た目
colorscheme elflord
"" 行表示
set number
"行番号の色。ColorSchemeによって反映されないのを防ぐために、autocmdを入れている
autocmd ColorScheme * highlight LineNr ctermfg=darkgrey
"autocmd ColorScheme * highlight CursorLineNr ctermfg=yellow
" 現在の行を強調表示
set cursorline
"" 現在の行を強調表示（縦）
set cursorcolumn
"" 行末の1文字先までカーソルを移動できるように
set virtualedit=onemore
" インデントはスマートインデント
set smartindent
" ビープ音を可視化
set visualbell
" 括弧入力時の対応する括弧を表示
set showmatch
" ステータスラインを常に表示
set laststatus=2
" ファイル名表示
set statusline+=%<%F
" 変更のチェック表示
set statusline+=%m
" 読み込み専用かどうか表示
set statusline+=%r
" ヘルプページなら[HELP]と表示
set statusline+=%h
" コマンドラインの補完
set wildmode=list:longest
" 折り返し時に表示行単位での移動できるようにする
nnoremap j gj
nnoremap k gk
" シンタックスハイライトの有効化
syntax enable
"モードによって背景色を変える
augroup InsertHook
    autocmd InsertEnter * hi Normal ctermbg=17 "挿入モード時の色
    autocmd InsertLeave * hi Normal ctermbg=16 "通常モード時の色
augroup END 
"jjと打つことでノーマルモードの切り替える
inoremap <silent> jj <ESC>

" Tab系
" 不可視文字を可視化(タブが「?-」と表示される)
"set list listchars=tab:\?\-
" Tab文字を半角スペースにする
set expandtab
" 行頭以外のTab文字の表示幅（スペースいくつ分）
set tabstop=4
" 行頭でのTab文字の表示幅
set shiftwidth=4
" 全角スペースの背景を白に変更
highlight FullWidthSpace ctermbg=white
match FullWidthSpace /　/ 

" 検索系
" 検索文字列が小文字の場合は大文字小文字を区別なく検索する
set ignorecase
" 検索文字列に大文字が含まれている場合は区別して検索する
set smartcase
" 検索文字列入力時に順次対象文字列にヒットさせる
set incsearch
" 検索語をハイライト表示
set hlsearch

