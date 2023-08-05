Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var sortable_1 = require("@dnd-kit/sortable");
var item_1 = tslib_1.__importDefault(require("./item"));
function SortableItem(_a) {
    var id = _a.id, index = _a.index, renderItem = _a.renderItem, disabled = _a.disabled, wrapperStyle = _a.wrapperStyle, innerWrapperStyle = _a.innerWrapperStyle;
    var _b = sortable_1.useSortable({ id: id, disabled: disabled }), attributes = _b.attributes, isSorting = _b.isSorting, isDragging = _b.isDragging, listeners = _b.listeners, setNodeRef = _b.setNodeRef, overIndex = _b.overIndex, transform = _b.transform, transition = _b.transition;
    return (<item_1.default forwardRef={setNodeRef} value={id} sorting={isSorting} renderItem={renderItem} index={index} transform={transform} transition={transition} listeners={listeners} attributes={attributes} wrapperStyle={wrapperStyle({ id: id, index: index, isDragging: isDragging, isSorting: isSorting })} innerWrapperStyle={innerWrapperStyle({
            id: id,
            index: index,
            isDragging: isDragging,
            isSorting: isSorting,
            overIndex: overIndex,
            isDragOverlay: false,
        })}/>);
}
exports.default = SortableItem;
//# sourceMappingURL=sortableItem.jsx.map