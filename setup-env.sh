export PYTHONPATH=$PYTHONPATH:`/usr/bin/python -c "import sys; print ':'.join( x for x in sys.path if x )"`

export DJANGO_SETTINGS_MODULE="zinc_saucier.settings"
