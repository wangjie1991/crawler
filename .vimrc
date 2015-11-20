"set directory=/tmp
"set exrc
set errorbells

"set autowrite
"set readonly
set number
set report=0
"set scroll=
set showmatch
"set warn

set autoindent
"set lisp
"set list
set shiftwidth=4
set tabstop=4
"set wrapmargin=0

"set ignorecase
set magic
set nowrapscan

"set novice
set prompt
"set taglength=0
"set tags
"set tagstack

"---- vim ----
set nocompatible
set autoread
"set comments=
"set directory=., ~/tmp, /tmp
"set fileformat=Unix/dos/mac
"set fileformats=Unix,dos,mac
"set nohidden
"set modifiable
"set nopaste
"set nosecure
"set mouse=a
"set mousehide
"set mousemodel=extend

"set background=dark
"set cursorcolumn
set cursorline
set ruler
set wrap
set linebreak
"set showbreak=
set laststatus=2
"set showmode
set scrolloff=3

"set cindent
"set cinkeys=0{,0},:,0#,!,o,O,e
"set cinoptions
"set cinwords=if, else, while, do, for, switch
"set smartindent
set expandtab
set smarttab
set softtabstop=4

"set completeopt
"set history=20
set hlsearch
set incsearch
"set nosmartcase

"set cmdheight=1
"set showcmd 
set wildmenu
set langmenu=zh_CN.UTF-8
set helplang=en
set termencoding=utf8
set encoding=utf8

"set makeef=/tmp/vim##.err
"set makeprg=make

"set nobackup
"set backupdir=., ~/tmp, ~/
"set backupext=~
"set writebackup


"colorscheme desert


"进行版权声明的设置
"添加或更新头
map <F4> :call TitleDet()<cr>'s
function AddTitle()
    call append(0,"/*=============================================================================")
    call append(1,"#")
    call append(2,"# Author: dantezhu - dantezhu@vip.qq.com")
    call append(3,"#")
    call append(4,"# QQ : 327775604")
    call append(5,"#")
    call append(6,"# Last modified: ".strftime("%Y-%m-%d %H:%M"))
    call append(7,"#")
    call append(8,"# Filename: ".expand("%:t"))
    call append(9,"#")
    call append(10,"# Description: ")
    call append(11,"#")
    call append(12,"=============================================================================*/")
    echohl WarningMsg | echo "Successful in adding the copyright." | echohl None
endf
"更新最近修改时间和文件名
function UpdateTitle()
    normal m'
    execute '/# *Last modified:/s@:.*$@\=strftime(":\t%Y-%m-%d %H:%M")@'
    normal ''
    normal mk
    execute '/# *Filename:/s@:.*$@\=":\t\t".expand("%:t")@'
    execute "noh"
    normal 'k
    echohl WarningMsg | echo "Successful in updating the copy right." | echohl None
endfunction
"判断前10行代码里面，是否有Last modified这个单词，
"如果没有的话，代表没有添加过作者信息，需要新添加；
"如果有的话，那么只需要更新即可
function TitleDet()
    let n=1
    "默认为添加
    while n < 10
        let line = getline(n)
        if line =~ '^\#\s*\S*Last\smodified:\S*.*$'
            call UpdateTitle()
            return
        endif
        let n = n + 1
    endwhile
    call AddTitle()
endfunction
