Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var checkboxFancy_1 = tslib_1.__importDefault(require("app/components/checkboxFancy/checkboxFancy"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function FilterSection(_a) {
    var id = _a.id, label = _a.label, items = _a.items, toggleSection = _a.toggleSection, toggleFilter = _a.toggleFilter;
    var checkedItemsCount = items.filter(function (item) { return item.checked; }).length;
    return (<react_1.Fragment>
      <Header>
        <span>{label}</span>
        <checkboxFancy_1.default isChecked={checkedItemsCount === items.length} isIndeterminate={checkedItemsCount > 0 && checkedItemsCount !== items.length} onClick={function (event) {
            event.stopPropagation();
            toggleSection(id);
        }}/>
      </Header>
      {items
            .filter(function (item) { return !item.filtered; })
            .map(function (item) { return (<ListItem key={item.value} isChecked={item.checked} onClick={function (event) {
                event.stopPropagation();
                toggleFilter(id, item.value);
            }}>
            <TeamName>{item.label}</TeamName>
            <checkboxFancy_1.default isChecked={item.checked}/>
          </ListItem>); })}
    </react_1.Fragment>);
}
var Filter = /** @class */ (function (_super) {
    tslib_1.__extends(Filter, _super);
    function Filter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.toggleFilter = function (sectionId, value) {
            var _a = _this.props, onFilterChange = _a.onFilterChange, dropdownSections = _a.dropdownSections;
            var section = dropdownSections.find(function (dropdownSection) { return dropdownSection.id === sectionId; });
            var newSelection = new Set(section.items.filter(function (item) { return item.checked; }).map(function (item) { return item.value; }));
            if (newSelection.has(value)) {
                newSelection.delete(value);
            }
            else {
                newSelection.add(value);
            }
            onFilterChange(sectionId, newSelection);
        };
        _this.toggleSection = function (sectionId) {
            var onFilterChange = _this.props.onFilterChange;
            var section = _this.props.dropdownSections.find(function (dropdownSection) { return dropdownSection.id === sectionId; });
            var activeItems = section.items.filter(function (item) { return item.checked; });
            var newSelection = section.items.length === activeItems.length
                ? new Set()
                : new Set(section.items.map(function (item) { return item.value; }));
            onFilterChange(sectionId, newSelection);
        };
        _this.getNumberOfActiveFilters = function () {
            return _this.props.dropdownSections
                .map(function (section) { return section.items; })
                .flat()
                .filter(function (item) { return item.checked; }).length;
        };
        return _this;
    }
    Filter.prototype.render = function () {
        var _this = this;
        var _a = this.props, dropdownItems = _a.dropdownSections, header = _a.header;
        var checkedQuantity = this.getNumberOfActiveFilters();
        var dropDownButtonProps = {
            children: locale_1.t('Filter'),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        if (checkedQuantity > 0) {
            dropDownButtonProps.children = locale_1.tn('%s Active Filter', '%s Active Filters', checkedQuantity);
            dropDownButtonProps.hasDarkBorderBottomColor = true;
        }
        return (<dropdownControl_1.default menuWidth="240px" blendWithActor alwaysRenderMenu={false} button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} icon={<icons_1.IconFilter size="xs"/>} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
            {dropDownButtonProps.children}
          </StyledDropdownButton>);
            }}>
        {function (_a) {
                var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps;
                return (<MenuContent {...getMenuProps()} isOpen={isOpen} blendCorner alignMenu="left" width="240px">
            <List>
              {header}
              {dropdownItems.map(function (section) { return (<FilterSection key={section.id} {...section} toggleSection={_this.toggleSection} toggleFilter={_this.toggleFilter}/>); })}
            </List>
          </MenuContent>);
            }}
      </dropdownControl_1.default>);
    };
    return Filter;
}(react_1.Component));
var MenuContent = styled_1.default(dropdownControl_1.Content)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  max-height: 290px;\n  overflow-y: auto;\n"], ["\n  max-height: 290px;\n  overflow-y: auto;\n"])));
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), space_1.default(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(2), function (p) { return p.theme.border; });
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n"], ["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.dropdown; });
var List = styled_1.default('ul')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled_1.default('li')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space_1.default(1), space_1.default(1), space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, checkboxFancy_1.default, function (p) { return (p.isChecked ? 1 : 0.3); }, checkboxFancy_1.default, function (p) { return p.theme.blue300; });
var TeamName = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis_1.default);
exports.default = Filter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=filter.jsx.map