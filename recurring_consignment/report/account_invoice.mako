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

<!-- Resume -->
        <table border="1" cellspacing="0" style="width:100%;">
            <tr>
                <th colspan="4" style="background-color:#AAEA28">
                    <h2>Justificatif de facture de commissions</h2>
                </th>
            </tr>
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
                <th colspan="4" style="background-color:#AAEA28">
                    <h2>Informations générales</h2>
                </th>
                

            </tr>
            <tr>
                <td colspan="6" style="font-size: 10px; text-align:center;">
                    Note : La commission est appliquée sur le chiffre d'affaire Hors Taxe
                </td>
            </tr>
    %if invoice.number:
            <tr>
                <th>Facture de commission</th>
                <td>${invoice.number}</td>
                <th>Période</th>
                <td>${invoice.period_id.name}</td>
            </tr>
    %endif
            <tr>
                <th>Taux de commission</th>
                <td>${invoice.partner_id.consignment_commission} %</td>
                <th colspan="2" />
            </tr>
            <tr>
<%
    res = invoice.commission_information_summary
    total = 0
%>
                <th colspan="4" style="background-color:#AAEA28">
                    <h2>Encaissements réalisés pour le compte du dépôt vendeur</h2>
                </th>

            </tr>
            <tr>
                <th colspan="2">Libellé</th>
                <th>Commissionné</th>
                <th>Valeur</th>
            </tr>
    %for line in res :
<%
        total += line['amount']
%>
            <tr>
                <td colspan="2">${line['name']}</td>
                <td style="text-align:right">
        %if line['is_commission']:
                Oui
        %endif
                </td>
                <td style="text-align:right">${'%.2f' % line['amount']} €</td>

            </tr>
    %endfor
            <tr>
                <th colspan="3" style="text-align:right">Total TTC</th>
                <td style="text-align:right; background-color:#CCF">${'%.2f' % total} €</td>
            </tr>

            <tr>
                <th colspan="4"  style="background-color:#AAEA28">
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
                <td style="text-align:right; background-color:#CCF">${'%.2f' % invoice.amount_total} €</td>
            </tr>

            <tr>
                <th colspan="4" style="background-color:#AAEA28">
                    <h2>A reverser</h2>
                </th>
            </tr>
            <tr>
                <th colspan="3" style="text-align:right">Total TTC</th>
                <td style="text-align:right; background-color:#CCF">${'%.2f' % (total - invoice.amount_total)} €</td>
            </tr>
        </table>

<!-- Detail Comptable -->
        <table border="1" cellspacing="0" style="page-break-before:always; width:100%;">
            <tr>
                <th colspan="6" style="background-color:#AAEA28">
                    <h2>Détail des pièces comptables</h2>
                </th>
            </tr>
            <tr>
                <td colspan="6" style="font-size: 10px; text-align:center;">
                    Note : les valeurs aux débits peuvent correspondre à un retour de produit de la part du client, à un retour de consigne dans le cas de produit consigné, ou à l'annulation de tout ou partie d'une vente suite à une erreur de saisie.
                </td>
            </tr>
            <tr>
                <th>Date</th>
                <th>Pièce comptable</th>
                <th>Libellé</th>
                <th>Com.</th>
                <th>Débit</th>
                <th>Crédit</th>
            </tr>
<%
    lines = invoice.commission_information_detail
    current = ''
    color = '#FFF'
    total_debit = 0
    total_credit = 0
%>
    %for line in lines:
<%
        new = (current != line['name'])
        current = line['name']
        total_debit += line['debit']
        total_credit += line['credit']
        if new:
            color = (color == '#FFF') and '#DDD' or '#FFF'
%>
            <tr style="font-size: 12px; background-color:${color};page-break-inside: avoid;">
                <td>${line['date'][8:10]}/${line['date'][5:7]}/${line['date'][0:4]}</td>
                <td>${line['name']}</td>
                <td>${line['description']}</td>
                <td>
        %if line['is_commission']:
                Oui
        %endif
                </td>
        %if line['debit']:
                <td style="text-align:right">${'%.2f' % line['debit']} €</td>
                <td>&nbsp;</td>
        %else:
                <td>&nbsp;</td>
                <td style="text-align:right">${'%.2f' % line['credit']} €</td>
        %endif

            </tr>
    %endfor
            <tr>
                <th colspan="6" style="background-color:#AAEA28">Total</th>
            </tr>
            <tr style="font-size: 12px;">
                <th colspan="4">&nbsp;</th>
                <td style="text-align:right; background-color:#CCF">${'%.2f' % (total_debit)} €</td>
                <td style="text-align:right; background-color:#CCF">${'%.2f' % (total_credit)} €</td>
            </tr>
        </table>

<!-- Detail Produits -->

        <table border="1" cellspacing="0" style="page-break-before:always; width:100%;">
            <tr>
                <th colspan="7" style="background-color:#AAEA28">
                    <h2>Détail des produits</h2>
                </th>
            </tr>
            <tr>
                <th style="width: 15%">Code</th>
                <th style="width: 31%">Produit</th>
                <th style="width: 10%">Qté</th>
                <th style="width: 10%">Prix Unitaire</th>
                <th style="width: 10%">Remise</th>
                <th style="width: 12%">Total HT</th>
                <th style="width: 12%">Total TTC</th>
            </tr>
<%
    lines = invoice.product_detail
    current = ''
    color = '#FFF'
    total_vat_excl = 0
    total_vat_incl = 0
%>
    %for line in lines:
<%
        new = (current != line['product_code'])
        current = line['product_code']
        if new:
            color = (color == '#FFF') and '#DDD' or '#FFF'
        total_vat_excl += line['total_vat_excl']
        total_vat_incl += line['total_vat_incl']
%>
            <tr style="font-size: 12px; background-color:${color};page-break-inside: avoid;">
                <td>${line['product_code']}</td>
                <td>${line['product_name']}</td>
                <td style="text-align:right">${'%.3f' % line['quantity']}</td>
                <td style="text-align:right">${'%.2f' % line['price_unit']} €</td>
                <td style="text-align:right">${'%.2f' % line['discount']} %</td>
                <td style="text-align:right">${'%.2f' % line['total_vat_excl']} €</td>
                <td style="text-align:right">${'%.2f' % line['total_vat_incl']} €</td>
            </tr>
    %endfor
            <tr>
                <th colspan="7" style="background-color:#AAEA28">Total</th>
            </tr>
            <tr style="font-size: 12px;">
                <th colspan="5">&nbsp;</th>
                <td style="text-align:right; background-color:#CCF">${'%.2f' % (total_vat_excl)} €</td>
                <td style="text-align:right; background-color:#CCF">${'%.2f' % (total_vat_incl)} €</td>
            </tr>
        </table>
%endfor
    </body>
</html>

