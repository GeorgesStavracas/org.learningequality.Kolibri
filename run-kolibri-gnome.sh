#!/bin/sh

XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
KOLIBRI_HOME="${KOLIBRI_HOME:-$XDG_DATA_HOME/kolibri}"

export KOLIBRI_HOME

OLD_KOLIBRI_HOME="${XDG_DATA_HOME}/../.kolibri"

if [[ -d "${OLD_KOLIBRI_HOME}" && ! -f ${KOLIBRI_HOME} ]]; then
    echo "Moving KOLIBRI_HOME from '${OLD_KOLIBRI_HOME}' to '${KOLIBRI_HOME}'"
    mv "${OLD_KOLIBRI_HOME}" "${KOLIBRI_HOME}"
fi

kolibri-gnome "$@"

