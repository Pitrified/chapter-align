# https://stackoverflow.com/a/18460742
for i in {0003..0005} ; do
    # echo "$i"
    echo "ch_$i.xhtml"
    cp ch_tmpl.xhtml "ch_$i.xhtml"
done
