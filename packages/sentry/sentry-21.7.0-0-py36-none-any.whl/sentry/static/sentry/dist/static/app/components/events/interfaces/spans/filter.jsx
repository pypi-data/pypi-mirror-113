Object.defineProperty(exports, "__esModule", { value: true });
exports.toggleAllFilters = exports.toggleFilter = exports.noFilter = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var checkboxFancy_1 = tslib_1.__importDefault(require("app/components/checkboxFancy/checkboxFancy"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = tslib_1.__importDefault(require("app/components/dropdownControl"));
var utils_1 = require("app/components/performance/waterfall/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.noFilter = {
    type: 'no_filter',
};
var Filter = /** @class */ (function (_super) {
    tslib_1.__extends(Filter, _super);
    function Filter() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Filter.prototype.isOperationNameActive = function (operationName) {
        var operationNameFilter = this.props.operationNameFilter;
        if (operationNameFilter.type === 'no_filter') {
            return false;
        }
        // invariant: operationNameFilter.type === 'active_filter'
        return operationNameFilter.operationNames.has(operationName);
    };
    Filter.prototype.getNumberOfActiveFilters = function () {
        var operationNameFilter = this.props.operationNameFilter;
        if (operationNameFilter.type === 'no_filter') {
            return 0;
        }
        return operationNameFilter.operationNames.size;
    };
    Filter.prototype.render = function () {
        var _this = this;
        var operationNameCounts = this.props.operationNameCounts;
        if (operationNameCounts.size === 0) {
            return null;
        }
        var checkedQuantity = this.getNumberOfActiveFilters();
        var dropDownButtonProps = {
            children: (<React.Fragment>
          <icons_1.IconFilter size="xs"/>
          <FilterLabel>{locale_1.t('Filter')}</FilterLabel>
        </React.Fragment>),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        if (checkedQuantity > 0) {
            dropDownButtonProps.children = (<span>{locale_1.tn('%s Active Filter', '%s Active Filters', checkedQuantity)}</span>);
            dropDownButtonProps.priority = 'primary';
            dropDownButtonProps.hasDarkBorderBottomColor = true;
        }
        return (<Wrapper data-test-id="op-filter-dropdown">
        <dropdownControl_1.default menuWidth="240px" blendWithActor button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
              {dropDownButtonProps.children}
            </StyledDropdownButton>);
            }}>
          <MenuContent onClick={function (event) {
                // propagated clicks will dismiss the menu; we stop this here
                event.stopPropagation();
            }}>
            <Header>
              <span>{locale_1.t('Operation')}</span>
              <checkboxFancy_1.default isChecked={checkedQuantity > 0} isIndeterminate={checkedQuantity > 0 && checkedQuantity !== operationNameCounts.size} onClick={function (event) {
                event.stopPropagation();
                _this.props.toggleAllOperationNameFilters();
            }}/>
            </Header>
            <List>
              {Array.from(operationNameCounts, function (_a) {
                var _b = tslib_1.__read(_a, 2), operationName = _b[0], operationCount = _b[1];
                var isActive = _this.isOperationNameActive(operationName);
                return (<ListItem key={operationName} isChecked={isActive}>
                    <OperationDot backgroundColor={utils_1.pickBarColour(operationName)}/>
                    <OperationName>{operationName}</OperationName>
                    <OperationCount>{operationCount}</OperationCount>
                    <checkboxFancy_1.default isChecked={isActive} onClick={function (event) {
                        event.stopPropagation();
                        _this.props.toggleOperationNameFilter(operationName);
                    }}/>
                  </ListItem>);
            })}
            </List>
          </MenuContent>
        </dropdownControl_1.default>
      </Wrapper>);
    };
    return Filter;
}(React.Component));
var FilterLabel = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var Wrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"], ["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  max-width: 200px;\n\n  &:hover,\n  &:active {\n    ", "\n  }\n\n  ", "\n"], ["\n  white-space: nowrap;\n  max-width: 200px;\n\n  &:hover,\n  &:active {\n    ", "\n  }\n\n  ", "\n"])), function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n          border-bottom-color: " + p.theme.button.primary.border + ";\n        ";
}, function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n      border-bottom-color: " + p.theme.button.primary.border + ";\n    ";
});
var MenuContent = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  max-height: 250px;\n  overflow-y: auto;\n  border-top: 1px solid ", ";\n"], ["\n  max-height: 250px;\n  overflow-y: auto;\n  border-top: 1px solid ", ";\n"])), function (p) { return p.theme.gray200; });
var Header = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), space_1.default(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(2), function (p) { return p.theme.border; });
var List = styled_1.default('ul')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled_1.default('li')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space_1.default(1), space_1.default(1), space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, checkboxFancy_1.default, function (p) { return (p.isChecked ? 1 : 0.3); }, checkboxFancy_1.default, function (p) { return p.theme.blue300; });
var OperationDot = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"], ["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"])), space_1.default(1), function (p) { return p.backgroundColor; });
var OperationName = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis_1.default);
var OperationCount = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
function toggleFilter(previousState, operationName) {
    if (previousState.type === 'no_filter') {
        return {
            type: 'active_filter',
            operationNames: new Set([operationName]),
        };
    }
    // invariant: previousState.type === 'active_filter'
    // invariant: previousState.operationNames.size >= 1
    var operationNames = previousState.operationNames;
    if (operationNames.has(operationName)) {
        operationNames.delete(operationName);
    }
    else {
        operationNames.add(operationName);
    }
    if (operationNames.size > 0) {
        return {
            type: 'active_filter',
            operationNames: operationNames,
        };
    }
    return {
        type: 'no_filter',
    };
}
exports.toggleFilter = toggleFilter;
function toggleAllFilters(previousState, operationNames) {
    if (previousState.type === 'no_filter') {
        return {
            type: 'active_filter',
            operationNames: new Set(operationNames),
        };
    }
    // invariant: previousState.type === 'active_filter'
    if (previousState.operationNames.size === operationNames.length) {
        // all filters were selected, so the next state should un-select all filters
        return {
            type: 'no_filter',
        };
    }
    // not all filters were selected, so the next state is to select all the remaining filters
    return {
        type: 'active_filter',
        operationNames: new Set(operationNames),
    };
}
exports.toggleAllFilters = toggleAllFilters;
exports.default = Filter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=filter.jsx.map