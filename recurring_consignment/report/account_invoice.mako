## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            body{
                font-family: arial, verdana, sans-serif;
                padding: 20px;
                font-size:medium;
            }

        </style>
    </head>
    <body>

    %for invoice in objects :

        <h1>Justificatif de facture de commissions</h1>
        <table border="1" cellspacing="0">
            <tr>
                <th colspan="2">Entre le Dépôt Vente</th>
                <th colspan="2">Et le Dépôt-Vendeur</th>
            </tr>
            <tr>
                <th>Nom</th>
                <td>${invoice.company_id.name}</td>
                <th>Nom</th>
                <td>${invoice.partner_id.name}</td>
            </tr>
            <tr>
                <th>Adresse</th>
                <td>${invoice.company_id.partner_id.contact_address}</td>
                <th>Adresse</th>
                <td>${invoice.partner_id.contact_address}</td>
            </tr>
            <tr>
                <th colspan="4">
                <h2>Informations générales</h2>
                </th>
            </tr>
            <tr>
                <th>Code comptable</th>
                <td>${invoice.account_id.code}</td>
                <th>Compte comptable</th>
                <td>${invoice.account_id.name}</td>
            </tr>
            <tr>
                <th>Facture de commission</th>
                <td>${invoice.number}</td>
                <th>Période</th>
                <td>${invoice.period_id.name}</td>
            </tr>
            <tr>
                <th>Taux de commission</th>
                <td>${invoice.partner_id.consignment_commission} %</td>
                <th colspan="2" />
            </tr>
            <tr>
<%
    res = invoice.commission_information
    total = 0
%>
                <th colspan="4">
                    <h2>Encaissements réalisés pour le compte du dépôt vendeur</h2>
                </th>

            </tr>
            <tr>
                <th colspan="2">Libellé</th>
                <th>Taux de commission</th>
                <th>Valeur</th>
            </tr>
    %for line in res :
<%
        total += line['amount']
%>
            <tr>
                <td colspan="2">${line['name']}</td>
                <td style="text-align:right">${'%.2f' % line['commission_rate']} %</td>
                <td style="text-align:right">${'%.2f' % line['amount']} €</td>

            </tr>
    %endfor
            <tr>
                <th colspan="3" style="text-align:right">Total TTC</th>
                <td style="text-align:right">${'%.2f' % total} €</td>
            </tr>

            <tr>
                <th colspan="4">
                    <h2>Commissions</h2>
                </th>
            </tr>
            <tr>
                <th colspan="2">Libellé</th>
                <th>HT</th>
                <th>TTC</th>
            </tr>
    %for invoice_line in invoice.invoice_line :
            <tr>
                <td colspan="2">
                    ${invoice_line.product_id.name}<br />
                    ${invoice_line.name}
                </td>
                <td style="text-align:right">${'%.2f' % invoice_line.price_subtotal} €</td>
                <td style="text-align:right">${'%.2f' % invoice_line.price_subtotal_taxinc} €</td>
            </tr>
    %endfor
            <tr>
                <th colspan="3" style="text-align:right">Total TTC</th>
                <td style="text-align:right">${'%.2f' % invoice.amount_total} €</td>
            </tr>

            <tr>
                <th colspan="4">
                    <h2>A reverser</h2>
                </th>
            </tr>
            <tr>
                <th colspan="3" style="text-align:right">Total TTC</th>
                <td style="text-align:right">${'%.2f' % (total - invoice.amount_total)} €</td>
            </tr>
        </table>



        <h1 style="page-break-before:always">Justificatif comptable</h1>
        <p>et son texte</p>
    %endfor
    </body>
</html>

