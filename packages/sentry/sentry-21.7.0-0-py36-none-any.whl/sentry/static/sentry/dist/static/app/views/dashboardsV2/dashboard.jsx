Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var core_1 = require("@dnd-kit/core");
var sortable_1 = require("@dnd-kit/sortable");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var tags_1 = require("app/actionCreators/tags");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var utils_1 = require("./widget/utils");
var addWidget_1 = tslib_1.__importStar(require("./addWidget"));
var sortableWidget_1 = tslib_1.__importDefault(require("./sortableWidget"));
var Dashboard = /** @class */ (function (_super) {
    tslib_1.__extends(Dashboard, _super);
    function Dashboard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleStartAdd = function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection;
            modal_1.openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
            });
        };
        _this.handleOpenWidgetBuilder = function () {
            var _a = _this.props, router = _a.router, paramDashboardId = _a.paramDashboardId, organization = _a.organization, location = _a.location;
            if (paramDashboardId) {
                router.push({
                    pathname: "/organizations/" + organization.slug + "/dashboard/" + paramDashboardId + "/widget/new/",
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
                });
                return;
            }
            router.push({
                pathname: "/organizations/" + organization.slug + "/dashboards/new/widget/new/",
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
            });
        };
        _this.handleAddComplete = function (widget) {
            _this.props.onUpdate(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(_this.props.dashboard.widgets)), [widget]));
        };
        _this.handleUpdateComplete = function (index) { return function (nextWidget) {
            var nextList = tslib_1.__spreadArray([], tslib_1.__read(_this.props.dashboard.widgets));
            nextList[index] = nextWidget;
            _this.props.onUpdate(nextList);
        }; };
        _this.handleDeleteWidget = function (index) { return function () {
            var nextList = tslib_1.__spreadArray([], tslib_1.__read(_this.props.dashboard.widgets));
            nextList.splice(index, 1);
            _this.props.onUpdate(nextList);
        }; };
        _this.handleEditWidget = function (widget, index) { return function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection, router = _a.router, location = _a.location, paramDashboardId = _a.paramDashboardId, onSetWidgetToBeUpdated = _a.onSetWidgetToBeUpdated;
            if (organization.features.includes('metrics')) {
                onSetWidgetToBeUpdated(widget);
                if (paramDashboardId) {
                    router.push({
                        pathname: "/organizations/" + organization.slug + "/dashboard/" + paramDashboardId + "/widget/" + index + "/edit/",
                        query: tslib_1.__assign(tslib_1.__assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
                    });
                    return;
                }
                router.push({
                    pathname: "/organizations/" + organization.slug + "/dashboards/new/widget/" + index + "/edit/",
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
                });
            }
            modal_1.openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                widget: widget,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
                onUpdateWidget: _this.handleUpdateComplete(index),
            });
        }; };
        return _this;
    }
    Dashboard.prototype.componentDidMount = function () {
        var isEditing = this.props.isEditing;
        // Load organization tags when in edit mode.
        if (isEditing) {
            this.fetchTags();
        }
    };
    Dashboard.prototype.componentDidUpdate = function (prevProps) {
        var isEditing = this.props.isEditing;
        // Load organization tags when going into edit mode.
        // We use tags on the add widget modal.
        if (prevProps.isEditing !== isEditing && isEditing) {
            this.fetchTags();
        }
    };
    Dashboard.prototype.fetchTags = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        tags_1.loadOrganizationTags(api, organization.slug, selection);
    };
    Dashboard.prototype.getWidgetIds = function () {
        return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(this.props.dashboard.widgets.map(function (widget, index) {
            return generateWidgetId(widget, index);
        }))), [
            addWidget_1.ADD_WIDGET_BUTTON_DRAG_ID,
        ]);
    };
    Dashboard.prototype.renderWidget = function (widget, index) {
        var isEditing = this.props.isEditing;
        var key = generateWidgetId(widget, index);
        var dragId = key;
        return (<sortableWidget_1.default key={key} widget={widget} dragId={dragId} isEditing={isEditing} onDelete={this.handleDeleteWidget(index)} onEdit={this.handleEditWidget(widget, index)}/>);
    };
    Dashboard.prototype.render = function () {
        var _this = this;
        var _a = this.props, isEditing = _a.isEditing, onUpdate = _a.onUpdate, widgets = _a.dashboard.widgets, organization = _a.organization;
        var items = this.getWidgetIds();
        return (<core_1.DndContext collisionDetection={core_1.closestCenter} onDragEnd={function (_a) {
                var over = _a.over, active = _a.active;
                var activeDragId = active.id;
                var getIndex = items.indexOf.bind(items);
                var activeIndex = activeDragId ? getIndex(activeDragId) : -1;
                if (over && over.id !== addWidget_1.ADD_WIDGET_BUTTON_DRAG_ID) {
                    var overIndex = getIndex(over.id);
                    if (activeIndex !== overIndex) {
                        onUpdate(sortable_1.arrayMove(widgets, activeIndex, overIndex));
                    }
                }
            }}>
        <WidgetContainer>
          <sortable_1.SortableContext items={items} strategy={sortable_1.rectSortingStrategy}>
            {widgets.map(function (widget, index) { return _this.renderWidget(widget, index); })}
            {isEditing && (<addWidget_1.default orgFeatures={organization.features} onAddWidget={this.handleStartAdd} onOpenWidgetBuilder={this.handleOpenWidgetBuilder}/>)}
          </sortable_1.SortableContext>
        </WidgetContainer>
      </core_1.DndContext>);
    };
    return Dashboard;
}(react_1.Component));
exports.default = withApi_1.default(withGlobalSelection_1.default(Dashboard));
var WidgetContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[3]; }, function (p) { return p.theme.breakpoints[4]; });
function generateWidgetId(widget, index) {
    return widget.id ? widget.id + "-index-" + index : "index-" + index;
}
var templateObject_1;
//# sourceMappingURL=dashboard.jsx.map