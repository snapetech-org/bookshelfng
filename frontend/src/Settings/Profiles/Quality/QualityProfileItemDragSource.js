import classNames from 'classnames';
import PropTypes from 'prop-types';
import React, { useRef } from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { QUALITY_PROFILE_ITEM } from 'Helpers/dragTypes';
import QualityProfileItem from './QualityProfileItem';
import QualityProfileItemGroup from './QualityProfileItemGroup';
import styles from './QualityProfileItemDragSource.css';

function QualityProfileItemDragSource(props) {
  const {
    editGroups,
    groupId,
    qualityId,
    name,
    allowed,
    items,
    qualityIndex,
    isDraggingUp,
    isDraggingDown,
    onCreateGroupPress,
    onDeleteGroupPress,
    onQualityProfileItemAllowedChange,
    onItemGroupAllowedChange,
    onItemGroupNameChange,
    onQualityProfileItemDragMove,
    onQualityProfileItemDragEnd
  } = props;
  const rowRef = useRef(null);

  const [{ isDragging }, dragRef] = useDrag(() => ({
    type: QUALITY_PROFILE_ITEM,
    item: () => ({
      editGroups,
      qualityIndex,
      groupId,
      qualityId,
      isGroup: !qualityId,
      name,
      allowed
    }),
    end: (item, monitor) => {
      onQualityProfileItemDragEnd(monitor.didDrop());
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging()
    })
  }), [props]);

  const [{ isOverCurrent }, dropRef] = useDrop(() => ({
    accept: QUALITY_PROFILE_ITEM,
    hover(item, monitor) {
      if (!monitor.isOver({ shallow: true }) || !rowRef.current) {
        return;
      }

      const {
        qualityIndex: dragQualityIndex,
        isGroup: isDragGroup
      } = monitor.getItem();
      const dropQualityIndex = props.qualityIndex;
      const isDropGroupItem = !!(props.qualityId && props.groupId);

      // The before placeholder becomes the first child while this row is an
      // active target above the dragged item.
      const childNodeIndex = props.isDraggingUp ? 1 : 0;
      const componentDOMNode = rowRef.current.children[childNodeIndex];

      if (!componentDOMNode) {
        return;
      }

      const hoverBoundingRect = componentDOMNode.getBoundingClientRect();
      const hoverMiddleY = (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      const clientOffset = monitor.getClientOffset();

      if (!clientOffset) {
        return;
      }

      const hoverClientY = clientOffset.y - hoverBoundingRect.top;

      // Don't show targets for dropping on self.
      if (dragQualityIndex === dropQualityIndex) {
        return;
      }

      // Don't allow a group to be dropped inside a group.
      if (isDragGroup && isDropGroupItem) {
        return;
      }

      let dropPosition = null;

      if (hoverClientY > hoverMiddleY) {
        dropPosition = 'below';
      } else if (hoverClientY < hoverMiddleY) {
        dropPosition = 'above';
      } else {
        return;
      }

      props.onQualityProfileItemDragMove({
        dragQualityIndex,
        dropQualityIndex,
        dropPosition
      });
    },
    collect: (monitor) => ({
      isOverCurrent: monitor.isOver({ shallow: true })
    })
  }), [props]);

  const isBefore = !isDragging && isDraggingUp && isOverCurrent;
  const isAfter = !isDragging && isDraggingDown && isOverCurrent;

  return (
    <div
      ref={(node) => {
        rowRef.current = node;
        dropRef(node);
      }}
      className={classNames(
        styles.qualityProfileItemDragSource,
        isBefore && styles.isDraggingUp,
        isAfter && styles.isDraggingDown
      )}
    >
      {
        isBefore &&
          <div
            className={classNames(
              styles.qualityProfileItemPlaceholder,
              styles.qualityProfileItemPlaceholderBefore
            )}
          />
      }

      {
        !!groupId && qualityId == null &&
          <QualityProfileItemGroup
            editGroups={editGroups}
            groupId={groupId}
            name={name}
            allowed={allowed}
            items={items}
            qualityIndex={qualityIndex}
            isDragging={isDragging}
            isDraggingUp={isDraggingUp}
            isDraggingDown={isDraggingDown}
            dragRef={dragRef}
            onDeleteGroupPress={onDeleteGroupPress}
            onQualityProfileItemAllowedChange={onQualityProfileItemAllowedChange}
            onItemGroupAllowedChange={onItemGroupAllowedChange}
            onItemGroupNameChange={onItemGroupNameChange}
            onQualityProfileItemDragMove={onQualityProfileItemDragMove}
            onQualityProfileItemDragEnd={onQualityProfileItemDragEnd}
          />
      }

      {
        qualityId != null &&
          <QualityProfileItem
            editGroups={editGroups}
            groupId={groupId}
            qualityId={qualityId}
            name={name}
            allowed={allowed}
            qualityIndex={qualityIndex}
            isDragging={isDragging}
            isOverCurrent={isOverCurrent}
            dragRef={dragRef}
            onCreateGroupPress={onCreateGroupPress}
            onQualityProfileItemAllowedChange={onQualityProfileItemAllowedChange}
          />
      }

      {
        isAfter &&
          <div
            className={classNames(
              styles.qualityProfileItemPlaceholder,
              styles.qualityProfileItemPlaceholderAfter
            )}
          />
      }
    </div>
  );
}

QualityProfileItemDragSource.propTypes = {
  editGroups: PropTypes.bool.isRequired,
  groupId: PropTypes.number,
  qualityId: PropTypes.number,
  name: PropTypes.string.isRequired,
  allowed: PropTypes.bool.isRequired,
  items: PropTypes.arrayOf(PropTypes.object),
  qualityIndex: PropTypes.string.isRequired,
  isDraggingUp: PropTypes.bool,
  isDraggingDown: PropTypes.bool,
  onCreateGroupPress: PropTypes.func,
  onDeleteGroupPress: PropTypes.func,
  onQualityProfileItemAllowedChange: PropTypes.func.isRequired,
  onItemGroupAllowedChange: PropTypes.func,
  onItemGroupNameChange: PropTypes.func,
  onQualityProfileItemDragMove: PropTypes.func.isRequired,
  onQualityProfileItemDragEnd: PropTypes.func.isRequired
};

export default QualityProfileItemDragSource;
