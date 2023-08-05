Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_dom_1 = require("react-dom");
var core_1 = require("@dnd-kit/core");
var sortable_1 = require("@dnd-kit/sortable");
var item_1 = tslib_1.__importDefault(require("./item"));
var sortableItem_1 = tslib_1.__importDefault(require("./sortableItem"));
var DraggableList = /** @class */ (function (_super) {
    tslib_1.__extends(DraggableList, _super);
    function DraggableList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleChangeActive = function (activeId) {
            _this.setState({ activeId: activeId });
        };
        return _this;
    }
    DraggableList.prototype.render = function () {
        var _this = this;
        var activeId = this.state.activeId;
        var _a = this.props, items = _a.items, onUpdateItems = _a.onUpdateItems, renderItem = _a.renderItem, disabled = _a.disabled, wrapperStyle = _a.wrapperStyle, innerWrapperStyle = _a.innerWrapperStyle;
        var getIndex = items.indexOf.bind(items);
        var activeIndex = activeId ? getIndex(activeId) : -1;
        return (<core_1.DndContext onDragStart={function (_a) {
                var active = _a.active;
                if (!active) {
                    return;
                }
                _this.handleChangeActive(active.id);
            }} onDragEnd={function (_a) {
                var over = _a.over;
                _this.handleChangeActive(undefined);
                if (over) {
                    var overIndex = getIndex(over.id);
                    if (activeIndex !== overIndex) {
                        onUpdateItems({
                            activeIndex: activeIndex,
                            overIndex: overIndex,
                            reorderedItems: sortable_1.arrayMove(items, activeIndex, overIndex),
                        });
                    }
                }
            }} onDragCancel={function () { return _this.handleChangeActive(undefined); }}>
        <sortable_1.SortableContext items={items} strategy={sortable_1.verticalListSortingStrategy}>
          {items.map(function (item, index) { return (<sortableItem_1.default key={item} id={item} index={index} renderItem={renderItem} disabled={disabled} wrapperStyle={wrapperStyle} innerWrapperStyle={innerWrapperStyle}/>); })}
        </sortable_1.SortableContext>
        {react_dom_1.createPortal(<core_1.DragOverlay>
            {activeId ? (<item_1.default value={items[activeIndex]} renderItem={renderItem} wrapperStyle={wrapperStyle({
                        id: items[activeIndex],
                        index: activeIndex,
                        isDragging: true,
                        isSorting: false,
                    })} innerWrapperStyle={innerWrapperStyle({
                        id: items[activeIndex],
                        index: activeIndex,
                        isSorting: activeId !== null,
                        isDragging: true,
                        overIndex: -1,
                        isDragOverlay: true,
                    })}/>) : null}
          </core_1.DragOverlay>, document.body)}
      </core_1.DndContext>);
    };
    DraggableList.defaultProps = {
        disabled: false,
        wrapperStyle: function () { return ({}); },
        innerWrapperStyle: function () { return ({}); },
    };
    return DraggableList;
}(react_1.Component));
exports.default = DraggableList;
//# sourceMappingURL=index.jsx.map