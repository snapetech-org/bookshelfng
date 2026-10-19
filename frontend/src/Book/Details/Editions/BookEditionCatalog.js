import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import Label from 'Components/Label';
import LoadingIndicator from 'Components/Loading/LoadingIndicator';
import TableRowCell from 'Components/Table/Cells/TableRowCell';
import Table from 'Components/Table/Table';
import TableBody from 'Components/Table/TableBody';
import TableRow from 'Components/Table/TableRow';
import createAjaxRequest from 'Utilities/createAjaxRequest';
import translate from 'Utilities/String/translate';
import styles from './BookEditionCatalog.css';

const columns = [
  { name: 'title', label: () => translate('Title'), isVisible: true, isSortable: false },
  { name: 'narrators', label: () => translate('EditionNarrators'), isVisible: true, isSortable: false },
  { name: 'production', label: () => translate('EditionProduction'), isVisible: true, isSortable: false },
  { name: 'abridgement', label: () => translate('EditionAbridgement'), isVisible: true, isSortable: false },
  { name: 'language', label: () => translate('Language'), isVisible: true, isSortable: false },
  { name: 'publisher', label: () => translate('Publisher'), isVisible: true, isSortable: false },
  { name: 'status', label: () => translate('Status'), isVisible: true, isSortable: false }
];

export function formatDuration(seconds) {
  if (!Number.isFinite(seconds) || seconds <= 0) {
    return null;
  }

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.round((seconds % 3600) / 60);
  return `${hours}h ${String(minutes).padStart(2, '0')}m`;
}

function NotProvided() {
  return <span className={styles.unknown}>{translate('EditionNotProvided')}</span>;
}

function productionLabel(production) {
  if (production === 'full-cast') {
    return translate('EditionFullCast');
  }

  return production === 'solo' ? translate('EditionSolo') : null;
}

function abridgementLabel(abridged) {
  if (abridged === 'abridged') {
    return translate('EditionAbridged');
  }

  return abridged === 'unabridged' ? translate('EditionUnabridged') : null;
}

function BookEditionCatalog({ bookId }) {
  const [state, setState] = useState({ isFetching: true, error: false, items: [] });

  useEffect(() => {
    const { request, abortRequest } = createAjaxRequest({
      url: `/book/${bookId}/editions/catalog`,
      dataType: 'json'
    });

    setState({ isFetching: true, error: false, items: [] });
    request.done((items) => setState({ isFetching: false, error: false, items: items || [] }));
    request.fail((xhr) => {
      if (xhr.aborted) {
        return;
      }

      setState({ isFetching: false, error: true, items: [] });
    });

    return abortRequest;
  }, [bookId]);

  const { isFetching, error, items } = state;

  if (isFetching) {
    return <LoadingIndicator />;
  }

  if (error) {
    return <div className={styles.message} role="alert">{translate('EditionCatalogFailed')}</div>;
  }

  if (!items.length) {
    return <div className={styles.message}>{translate('EditionCatalogEmpty')}</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.help}>{translate('EditionCatalogHelp')}</div>
      <Table columns={columns}>
        <TableBody>
          {items.map((edition) => {
            const production = edition.isEbook ? null : productionLabel(edition.production);
            const abridgement = edition.isEbook ? null : abridgementLabel(edition.abridged);

            return (
              <TableRow key={edition.editionId}>
                <TableRowCell className={styles.title}>{edition.title}</TableRowCell>
                <TableRowCell className={styles.narrators}>
                  {edition.narrators && edition.narrators.length ?
                    edition.narrators.join(', ') :
                    <NotProvided />}
                </TableRowCell>
                <TableRowCell className={styles.production}>
                  {production || <NotProvided />}
                </TableRowCell>
                <TableRowCell className={styles.abridgement}>
                  {abridgement || <NotProvided />}
                </TableRowCell>
                <TableRowCell className={styles.language}>
                  {edition.language || <NotProvided />}
                </TableRowCell>
                <TableRowCell className={styles.publisher}>
                  {edition.publisher || <NotProvided />}
                </TableRowCell>
                <TableRowCell className={styles.status}>
                  {edition.monitored && <Label kind="primary">{translate('EditionSelected')}</Label>}
                  {edition.owned && <Label kind="success">{translate('EditionOwned')}</Label>}
                </TableRowCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}

BookEditionCatalog.propTypes = {
  bookId: PropTypes.number.isRequired
};

export default BookEditionCatalog;
