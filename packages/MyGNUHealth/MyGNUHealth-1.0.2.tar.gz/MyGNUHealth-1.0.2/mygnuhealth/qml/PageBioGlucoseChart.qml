import QtQuick 2.7
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import org.kde.kirigami 2.5 as Kirigami
// import org.kde.quickcharts 1.0 as Charts
import GHBio 0.1

Kirigami.Page
{
id: glucosehist
title: qsTr("Glucose Level")
    GHBio { // GHBio object registered at main.py
        id: ghbio
    }

    ColumnLayout {
        spacing: 30
        Layout.fillWidth: true
        Layout.fillHeight: true

        Rectangle {
            id: glucosehistchart
            Layout.alignment: Qt.AlignCenter
            Layout.preferredWidth: 350
            Layout.preferredHeight: 250
            border.width: 2
            border.color: "#108498"

            Image {
                id:glucosehistplot
                anchors.fill: parent
                source: ghbio.glucoseplot
                fillMode:Image.PreserveAspectFit
            }
       }
    }
}

