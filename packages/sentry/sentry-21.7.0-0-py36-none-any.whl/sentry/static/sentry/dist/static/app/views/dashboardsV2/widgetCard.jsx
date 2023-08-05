Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var styles_1 = require("app/components/charts/styles");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var contextMenu_1 = tslib_1.__importDefault(require("./contextMenu"));
var utils_2 = require("./utils");
var widgetCardChart_1 = tslib_1.__importDefault(require("./widgetCardChart"));
var widgetQueries_1 = tslib_1.__importDefault(require("./widgetQueries"));
var WidgetCard = /** @class */ (function (_super) {
    tslib_1.__extends(WidgetCard, _super);
    function WidgetCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WidgetCard.prototype.shouldComponentUpdate = function (nextProps) {
        if (!isEqual_1.default(nextProps.widget, this.props.widget) ||
            !utils_1.isSelectionEqual(nextProps.selection, this.props.selection) ||
            this.props.isEditing !== nextProps.isEditing ||
            this.props.isSorting !== nextProps.isSorting ||
            this.props.hideToolbar !== nextProps.hideToolbar) {
            return true;
        }
        return false;
    };
    WidgetCard.prototype.renderToolbar = function () {
        var _a = this.props, onEdit = _a.onEdit, onDelete = _a.onDelete, draggableProps = _a.draggableProps, hideToolbar = _a.hideToolbar, isEditing = _a.isEditing;
        if (!isEditing) {
            return null;
        }
        return (<ToolbarPanel>
        <IconContainer style={{ visibility: hideToolbar ? 'hidden' : 'visible' }}>
          <IconClick>
            <StyledIconGrabbable color="textColor" {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.listeners} {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.attributes}/>
          </IconClick>
          <IconClick data-test-id="widget-edit" onClick={function () {
                onEdit();
            }}>
            <icons_1.IconEdit color="textColor"/>
          </IconClick>
          <IconClick data-test-id="widget-delete" onClick={function () {
                onDelete();
            }}>
            <icons_1.IconDelete color="textColor"/>
          </IconClick>
        </IconContainer>
      </ToolbarPanel>);
    };
    WidgetCard.prototype.renderContextMenu = function () {
        var _this = this;
        var _a = this.props, widget = _a.widget, selection = _a.selection, organization = _a.organization, showContextMenu = _a.showContextMenu;
        if (!showContextMenu) {
            return null;
        }
        var menuOptions = [];
        if (widget.displayType === 'table' &&
            organization.features.includes('discover-basic')) {
            // Open table widget in Discover
            if (widget.queries.length) {
                // We expect Table widgets to have only one query.
                var query = widget.queries[0];
                var eventView_1 = utils_2.eventViewFromWidget(widget.title, query, selection);
                menuOptions.push(<menuItem_1.default key="open-discover" onClick={function (event) {
                        event.preventDefault();
                        analytics_1.trackAnalyticsEvent({
                            eventKey: 'dashboards2.tablewidget.open_in_discover',
                            eventName: 'Dashboards2: Table Widget - Open in Discover',
                            organization_id: parseInt(_this.props.organization.id, 10),
                        });
                        react_router_1.browserHistory.push(eventView_1.getResultsViewUrlTarget(organization.slug));
                    }}>
            {locale_1.t('Open in Discover')}
          </menuItem_1.default>);
            }
        }
        if (!menuOptions.length) {
            return null;
        }
        return (<ContextWrapper>
        <contextMenu_1.default>{menuOptions}</contextMenu_1.default>
      </ContextWrapper>);
    };
    WidgetCard.prototype.render = function () {
        var _this = this;
        var _a = this.props, widget = _a.widget, api = _a.api, organization = _a.organization, selection = _a.selection, renderErrorMessage = _a.renderErrorMessage, location = _a.location, router = _a.router;
        return (<errorBoundary_1.default customComponent={<ErrorCard>{locale_1.t('Error loading widget data')}</ErrorCard>}>
        <StyledPanel isDragging={false}>
          <WidgetHeader>
            <WidgetTitle>{widget.title}</WidgetTitle>
            {this.renderContextMenu()}
          </WidgetHeader>
          <widgetQueries_1.default api={api} organization={organization} widget={widget} selection={selection}>
            {function (_a) {
                var tableResults = _a.tableResults, timeseriesResults = _a.timeseriesResults, errorMessage = _a.errorMessage, loading = _a.loading;
                return (<React.Fragment>
                  {typeof renderErrorMessage === 'function'
                        ? renderErrorMessage(errorMessage)
                        : null}
                  <widgetCardChart_1.default timeseriesResults={timeseriesResults} tableResults={tableResults} errorMessage={errorMessage} loading={loading} location={location} widget={widget} selection={selection} router={router} organization={organization}/>
                  {_this.renderToolbar()}
                </React.Fragment>);
            }}
          </widgetQueries_1.default>
        </StyledPanel>
      </errorBoundary_1.default>);
    };
    return WidgetCard;
}(React.Component));
exports.default = withApi_1.default(withOrganization_1.default(withGlobalSelection_1.default(ReactRouter.withRouter(WidgetCard))));
var ErrorCard = styled_1.default(placeholder_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.alert.error.border; }, function (p) { return p.theme.alert.error.textLight; }, function (p) { return p.theme.borderRadius; }, space_1.default(2));
var StyledPanel = styled_1.default(panels_1.Panel, {
    shouldForwardProp: function (prop) { return prop !== 'isDragging'; },
})(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  visibility: ", ";\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n"], ["\n  margin: 0;\n  visibility: ", ";\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n"])), function (p) { return (p.isDragging ? 'hidden' : 'visible'); });
var ToolbarPanel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n\n  background-color: ", ";\n  border-radius: ", ";\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n\n  background-color: ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.overlayBackgroundAlpha; }, function (p) { return p.theme.borderRadius; });
var IconContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin: 10px ", ";\n  touch-action: none;\n"], ["\n  display: flex;\n  margin: 10px ", ";\n  touch-action: none;\n"])), space_1.default(2));
var IconClick = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  padding: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"])), space_1.default(1));
var StyledIconGrabbable = styled_1.default(icons_1.IconGrabbable)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  &:hover {\n    cursor: grab;\n  }\n"], ["\n  &:hover {\n    cursor: grab;\n  }\n"])));
var WidgetTitle = styled_1.default(styles_1.HeaderTitle)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
var WidgetHeader = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n  width: 100%;\n  display: flex;\n  justify-content: space-between;\n"], ["\n  padding: ", " ", " 0 ", ";\n  width: 100%;\n  display: flex;\n  justify-content: space-between;\n"])), space_1.default(2), space_1.default(3), space_1.default(3));
var ContextWrapper = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=widgetCard.jsx.map