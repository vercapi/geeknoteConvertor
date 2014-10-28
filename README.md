geeknoteConvertor
=================

### What is it for

It enables you to edit evernote notes in emacs org-mode via geeknote.

### How to use it

open emacs

open eshell (M-x eshell)

in eshell issue the following commands

'''
$ geeknote find schroot
Total found: 4
  1 : 13.05.2012  Schroot - Debian Wiki
  2 : 13.05.2012  schroot - chroot for any userseshe

$ geeknote edit 2
'''

The file will open in emacs. You can edit it there.
Once finished just save and close the file.

### Install

#### Python engine

Open a shell

```
$ git clone https://github.com/vercapi/geeknoteConvertor.git
```

Next move to the new direcotry

```
$ cd geeknoteConvertor
```

```
sudo python setup.py install
```

#### Integrate with emacs

Add the following lines to your emacs startup system for instance your .emancs file


```
(defun close-org-hook ()
 (remove-hook 'kill-buffer-hook 'close-org-hook)
   (if (is-org-file)
       (org-md-export-to-markdown))
   (add-hook 'kill-buffer-hook 'close-org-hook))

(defun is-org-file ()
 (if (and 
      (string-match ".org" (substring (if buffer-file-name buffer-file-name "nilfile") -4))
      (string= (buffer-mode) "org-mode"))
     t))

(add-hook 'kill-buffer-hook 'close-org-hook)

(defun buffer-mode ()
  (with-current-buffer (current-buffer)
     major-mode))

(server-start)
```

##### Configure geeknote

In a shell

```
$ geeknote settings --editor gnconvertor
```