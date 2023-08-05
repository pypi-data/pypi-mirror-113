Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var similarSpectrum_1 = tslib_1.__importDefault(require("app/components/similarSpectrum"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var item_1 = tslib_1.__importDefault(require("./item"));
var toolbar_1 = tslib_1.__importDefault(require("./toolbar"));
var List = /** @class */ (function (_super) {
    tslib_1.__extends(List, _super);
    function List() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showAllItems: false,
        };
        _this.renderEmpty = function () { return (<panels_1.Panel>
      <panels_1.PanelBody>
        <emptyStateWarning_1.default small withIcon={false}>
          {locale_1.t('No issues with a similar stack trace have been found.')}
        </emptyStateWarning_1.default>
      </panels_1.PanelBody>
    </panels_1.Panel>); };
        _this.handleShowAll = function () {
            _this.setState({ showAllItems: true });
        };
        return _this;
    }
    List.prototype.render = function () {
        var _a = this.props, orgId = _a.orgId, groupId = _a.groupId, project = _a.project, items = _a.items, filteredItems = _a.filteredItems, pageLinks = _a.pageLinks, onMerge = _a.onMerge, v2 = _a.v2;
        var showAllItems = this.state.showAllItems;
        var hasHiddenItems = !!filteredItems.length;
        var hasResults = items.length > 0 || hasHiddenItems;
        var itemsWithFiltered = items.concat((showAllItems && filteredItems) || []);
        if (!hasResults) {
            return this.renderEmpty();
        }
        return (<react_1.Fragment>
        <Header>
          <similarSpectrum_1.default />
        </Header>

        <panels_1.Panel>
          <toolbar_1.default v2={v2} onMerge={onMerge}/>

          <panels_1.PanelBody>
            {itemsWithFiltered.map(function (item) { return (<item_1.default key={item.issue.id} orgId={orgId} v2={v2} groupId={groupId} project={project} {...item}/>); })}

            {hasHiddenItems && !showAllItems && (<Footer>
                <button_1.default onClick={this.handleShowAll}>
                  {locale_1.t('Show %s issues below threshold', filteredItems.length)}
                </button_1.default>
              </Footer>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={pageLinks}/>
      </react_1.Fragment>);
    };
    List.defaultProps = {
        filteredItems: [],
    };
    return List;
}(react_1.Component));
exports.default = List;
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var Footer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"])), space_1.default(1.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=list.jsx.map