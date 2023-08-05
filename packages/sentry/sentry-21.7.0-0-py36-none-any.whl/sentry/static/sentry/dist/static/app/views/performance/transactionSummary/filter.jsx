Object.defineProperty(exports, "__esModule", { value: true });
exports.filterToLocationQuery = exports.decodeFilterFromLocation = exports.stringToFilter = exports.filterToColour = exports.filterToSearchConditions = exports.filterToField = exports.spanOperationBreakdownSingleColumns = exports.SpanOperationBreakdownFilter = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = require("app/components/assistant/guideAnchor");
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = tslib_1.__importDefault(require("app/components/dropdownControl"));
var utils_1 = require("app/components/performance/waterfall/utils");
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var queryString_1 = require("app/utils/queryString");
var latencyChart_1 = require("./latencyChart");
// Make sure to update other instances like trends column fields, discover field types.
var SpanOperationBreakdownFilter;
(function (SpanOperationBreakdownFilter) {
    SpanOperationBreakdownFilter["None"] = "none";
    SpanOperationBreakdownFilter["Http"] = "http";
    SpanOperationBreakdownFilter["Db"] = "db";
    SpanOperationBreakdownFilter["Browser"] = "browser";
    SpanOperationBreakdownFilter["Resource"] = "resource";
})(SpanOperationBreakdownFilter = exports.SpanOperationBreakdownFilter || (exports.SpanOperationBreakdownFilter = {}));
var OPTIONS = [
    SpanOperationBreakdownFilter.Http,
    SpanOperationBreakdownFilter.Db,
    SpanOperationBreakdownFilter.Browser,
    SpanOperationBreakdownFilter.Resource,
];
exports.spanOperationBreakdownSingleColumns = OPTIONS.map(function (o) { return "spans." + o; });
var Filter = /** @class */ (function (_super) {
    tslib_1.__extends(Filter, _super);
    function Filter() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Filter.prototype.render = function () {
        var _a = this.props, currentFilter = _a.currentFilter, onChangeFilter = _a.onChangeFilter, organization = _a.organization;
        if (!organization.features.includes('performance-ops-breakdown')) {
            return null;
        }
        var dropDownButtonProps = {
            children: (<React.Fragment>
          <icons_1.IconFilter size="xs"/>
          <FilterLabel>
            {currentFilter === SpanOperationBreakdownFilter.None
                    ? locale_1.t('Filter')
                    : locale_1.tct('Filter - [operationName]', {
                        operationName: currentFilter,
                    })}
          </FilterLabel>
        </React.Fragment>),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        return (<guideAnchor_1.GuideAnchor target="span_op_breakdowns_filter" position="top">
        <Wrapper>
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
              <Header onClick={function (event) {
                event.stopPropagation();
                onChangeFilter(SpanOperationBreakdownFilter.None);
            }}>
                <HeaderTitle>{locale_1.t('Operation')}</HeaderTitle>
                <radio_1.default radioSize="small" checked={SpanOperationBreakdownFilter.None === currentFilter}/>
              </Header>
              <List>
                {Array.from(tslib_1.__spreadArray([], tslib_1.__read(OPTIONS)), function (filterOption, index) {
                var operationName = filterOption;
                return (<ListItem key={String(index)} isChecked={false} onClick={function (event) {
                        event.stopPropagation();
                        onChangeFilter(filterOption);
                    }}>
                      <OperationDot backgroundColor={utils_1.pickBarColour(operationName)}/>
                      <OperationName>{operationName}</OperationName>
                      <radio_1.default radioSize="small" checked={filterOption === currentFilter}/>
                    </ListItem>);
            })}
              </List>
            </MenuContent>
          </dropdownControl_1.default>
        </Wrapper>
      </guideAnchor_1.GuideAnchor>);
    };
    return Filter;
}(React.Component));
var FilterLabel = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var Wrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"], ["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ", "\n  }\n\n  ", "\n"], ["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ", "\n  }\n\n  ", "\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) {
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
var HeaderTitle = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var List = styled_1.default('ul')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled_1.default('li')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space_1.default(1), space_1.default(1), space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.blue300; });
var OperationDot = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"], ["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"])), space_1.default(1), function (p) { return p.backgroundColor; });
var OperationName = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis_1.default);
function filterToField(option) {
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return undefined;
        default: {
            return "spans." + option;
        }
    }
}
exports.filterToField = filterToField;
function filterToSearchConditions(option, location) {
    var field = filterToField(option);
    if (!field) {
        field = 'transaction.duration';
    }
    // Add duration search conditions implicitly
    var _a = latencyChart_1.decodeHistogramZoom(location), min = _a.min, max = _a.max;
    var query = '';
    if (typeof min === 'number') {
        query = query + " " + field + ":>" + min + "ms";
    }
    if (typeof max === 'number') {
        query = query + " " + field + ":<" + max + "ms";
    }
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return query ? query.trim() : undefined;
        default: {
            return (query + " has:" + filterToField(option)).trim();
        }
    }
}
exports.filterToSearchConditions = filterToSearchConditions;
function filterToColour(option) {
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return utils_1.pickBarColour('');
        default: {
            return utils_1.pickBarColour(option);
        }
    }
}
exports.filterToColour = filterToColour;
function stringToFilter(option) {
    if (Object.values(SpanOperationBreakdownFilter).includes(option)) {
        return option;
    }
    return SpanOperationBreakdownFilter.None;
}
exports.stringToFilter = stringToFilter;
function decodeFilterFromLocation(location) {
    return stringToFilter(queryString_1.decodeScalar(location.query.breakdown, SpanOperationBreakdownFilter.None));
}
exports.decodeFilterFromLocation = decodeFilterFromLocation;
function filterToLocationQuery(option) {
    return {
        breakdown: option,
    };
}
exports.filterToLocationQuery = filterToLocationQuery;
exports.default = Filter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=filter.jsx.map