Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var groupingComponent_1 = require("./groupingComponent");
var GroupingComponentFrames = /** @class */ (function (_super) {
    tslib_1.__extends(GroupingComponentFrames, _super);
    function GroupingComponentFrames() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: true,
        };
        return _this;
    }
    GroupingComponentFrames.prototype.render = function () {
        var _this = this;
        var _a = this.props, items = _a.items, maxVisibleItems = _a.maxVisibleItems;
        var collapsed = this.state.collapsed;
        var isCollapsable = items.length > maxVisibleItems;
        return (<React.Fragment>
        {items.map(function (item, index) {
                if (!collapsed || index < maxVisibleItems) {
                    return (<groupingComponent_1.GroupingComponentListItem isCollapsable={isCollapsable} key={index}>
                {item}
              </groupingComponent_1.GroupingComponentListItem>);
                }
                if (index === maxVisibleItems) {
                    return (<groupingComponent_1.GroupingComponentListItem key={index}>
                <ToggleCollapse size="small" priority="link" icon={<icons_1.IconAdd size="8px"/>} onClick={function () { return _this.setState({ collapsed: false }); }}>
                  {locale_1.tct('show [numberOfFrames] similiar', {
                            numberOfFrames: items.length - maxVisibleItems,
                        })}
                </ToggleCollapse>
              </groupingComponent_1.GroupingComponentListItem>);
                }
                return null;
            })}

        {!collapsed && items.length > maxVisibleItems && (<groupingComponent_1.GroupingComponentListItem>
            <ToggleCollapse size="small" priority="link" icon={<icons_1.IconSubtract size="8px"/>} onClick={function () { return _this.setState({ collapsed: true }); }}>
              {locale_1.tct('collapse [numberOfFrames] similiar', {
                    numberOfFrames: items.length - maxVisibleItems,
                })}
            </ToggleCollapse>
          </groupingComponent_1.GroupingComponentListItem>)}
      </React.Fragment>);
    };
    GroupingComponentFrames.defaultProps = {
        maxVisibleItems: 2,
    };
    return GroupingComponentFrames;
}(React.Component));
var ToggleCollapse = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n  color: ", ";\n"], ["\n  margin: ", " 0;\n  color: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.linkColor; });
exports.default = GroupingComponentFrames;
var templateObject_1;
//# sourceMappingURL=groupingComponentFrames.jsx.map