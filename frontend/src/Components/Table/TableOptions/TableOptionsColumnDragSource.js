import classNames from 'classnames';
import PropTypes from 'prop-types';
import React, { useRef } from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { TABLE_COLUMN } from 'Helpers/dragTypes';
import TableOptionsColumn from './TableOptionsColumn';
import styles from './TableOptionsColumnDragSource.css';

function TableOptionsColumnDragSource(props) {
  const {
    name,
    label,
    isVisible,
    isModifiable,
    index,
    isDraggingUp,
    isDraggingDown,
    onVisibleChange
  } = props;
  const rowRef = useRef(null);

  const [{ isDragging }, dragRef] = useDrag(() => ({
    type: TABLE_COLUMN,
    item: () => props,
    end: (item, monitor) => {
      props.onColumnDragEnd(monitor.getItem(), monitor.didDrop());
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging()
    })
  }), [props]);

  const [{ isOver }, dropRef] = useDrop(() => ({
    accept: TABLE_COLUMN,
    hover(item, monitor) {
      if (!rowRef.current) {
        return;
      }

      const dragIndex = monitor.getItem().index;
      const hoverIndex = props.index;
      const hoverBoundingRect = rowRef.current.getBoundingClientRect();
      const hoverMiddleY = (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      const clientOffset = monitor.getClientOffset();
      const hoverClientY = clientOffset.y - hoverBoundingRect.top;

      if (dragIndex === hoverIndex) {
        return;
      }

      // When moving up, only trigger if drag position is above 50% and
      // when moving down, only trigger if drag position is below 50%.
      // If we're moving down the hoverIndex needs to be increased
      // by one so it's ordered properly. Otherwise the hoverIndex will work.

      // Dragging downwards
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) {
        return;
      }

      // Dragging upwards
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) {
        return;
      }

      props.onColumnDragMove(dragIndex, hoverIndex);
    },
    collect: (monitor) => ({
      isOver: monitor.isOver()
    })
  }), [props]);

  const isBefore = !isDragging && isDraggingUp && isOver;
  const isAfter = !isDragging && isDraggingDown && isOver;

  return (
    <div
      ref={(node) => {
        rowRef.current = node;
        dropRef(node);
      }}
      className={classNames(
        styles.columnDragSource,
        isBefore && styles.isDraggingUp,
        isAfter && styles.isDraggingDown
      )}
    >
      {
        isBefore &&
          <div
            className={classNames(
              styles.columnPlaceholder,
              styles.columnPlaceholderBefore
            )}
          />
      }

      <TableOptionsColumn
        name={name}
        label={typeof label === 'function' ? label() : label}
        isVisible={isVisible}
        isModifiable={isModifiable}
        index={index}
        isDragging={isDragging}
        isOver={isOver}
        dragRef={dragRef}
        onVisibleChange={onVisibleChange}
      />

      {
        isAfter &&
          <div
            className={classNames(
              styles.columnPlaceholder,
              styles.columnPlaceholderAfter
            )}
          />
      }
    </div>
  );
}

TableOptionsColumnDragSource.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.func]).isRequired,
  isVisible: PropTypes.bool.isRequired,
  isModifiable: PropTypes.bool.isRequired,
  index: PropTypes.number.isRequired,
  isDraggingUp: PropTypes.bool,
  isDraggingDown: PropTypes.bool,
  onVisibleChange: PropTypes.func.isRequired,
  onColumnDragMove: PropTypes.func.isRequired,
  onColumnDragEnd: PropTypes.func.isRequired
};

export default TableOptionsColumnDragSource;
