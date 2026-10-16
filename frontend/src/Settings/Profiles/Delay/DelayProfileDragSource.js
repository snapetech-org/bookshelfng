import classNames from 'classnames';
import PropTypes from 'prop-types';
import React, { useRef } from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { DELAY_PROFILE } from 'Helpers/dragTypes';
import DelayProfile from './DelayProfile';
import styles from './DelayProfileDragSource.css';

function DelayProfileDragSource(props) {
  const {
    id,
    order,
    isDraggingUp,
    isDraggingDown,
    onDelayProfileDragMove,
    onDelayProfileDragEnd,
    ...otherProps
  } = props;
  const rowRef = useRef(null);

  const [{ isDragging }, dragRef] = useDrag(() => ({
    type: DELAY_PROFILE,
    item: () => props,
    end: (item, monitor) => {
      onDelayProfileDragEnd(monitor.getItem(), monitor.didDrop());
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging()
    })
  }), [props]);

  const [{ isOver }, dropRef] = useDrop(() => ({
    accept: DELAY_PROFILE,
    hover(item, monitor) {
      if (!rowRef.current) {
        return;
      }

      const dragIndex = monitor.getItem().order;
      const hoverIndex = props.order;
      const hoverBoundingRect = rowRef.current.getBoundingClientRect();
      const hoverMiddleY = (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      const clientOffset = monitor.getClientOffset();

      if (!clientOffset) {
        return;
      }

      const hoverClientY = clientOffset.y - hoverBoundingRect.top;

      if (dragIndex === hoverIndex) {
        return;
      }

      // When moving up, only trigger if drag position is above 50% and
      // when moving down, only trigger if drag position is below 50%.
      // If we're moving down the hoverIndex needs to be increased
      // by one so it's ordered properly. Otherwise the hoverIndex will work.

      if (dragIndex < hoverIndex && hoverClientY > hoverMiddleY) {
        props.onDelayProfileDragMove(dragIndex, hoverIndex + 1);
      } else if (dragIndex > hoverIndex && hoverClientY < hoverMiddleY) {
        props.onDelayProfileDragMove(dragIndex, hoverIndex);
      }
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
        styles.delayProfileDragSource,
        isBefore && styles.isDraggingUp,
        isAfter && styles.isDraggingDown
      )}
    >
      {
        isBefore &&
          <div
            className={classNames(
              styles.delayProfilePlaceholder,
              styles.delayProfilePlaceholderBefore
            )}
          />
      }

      <DelayProfile
        id={id}
        order={order}
        isDragging={isDragging}
        isOver={isOver}
        {...otherProps}
        dragRef={dragRef}
      />

      {
        isAfter &&
          <div
            className={classNames(
              styles.delayProfilePlaceholder,
              styles.delayProfilePlaceholderAfter
            )}
          />
      }
    </div>
  );
}

DelayProfileDragSource.propTypes = {
  id: PropTypes.number.isRequired,
  order: PropTypes.number.isRequired,
  isDraggingUp: PropTypes.bool,
  isDraggingDown: PropTypes.bool,
  onDelayProfileDragMove: PropTypes.func.isRequired,
  onDelayProfileDragEnd: PropTypes.func.isRequired
};

export default DelayProfileDragSource;
