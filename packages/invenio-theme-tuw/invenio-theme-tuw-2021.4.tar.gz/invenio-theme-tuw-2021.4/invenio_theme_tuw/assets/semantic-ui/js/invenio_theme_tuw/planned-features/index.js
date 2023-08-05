// This file is part of InvenioRDM
// Copyright (C) 2021 TU Wien.
//
// Invenio Theme TUW is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("pf-link-a").addEventListener("click", function () {
        $("#pf-list").transition("zoom");
        $("#pf-link").show();
    });

    document.getElementById("pf-list-a").addEventListener("click", function () {
        $("#pf-list").transition("zoom");
        $("#pf-link").hide();
    });
});
