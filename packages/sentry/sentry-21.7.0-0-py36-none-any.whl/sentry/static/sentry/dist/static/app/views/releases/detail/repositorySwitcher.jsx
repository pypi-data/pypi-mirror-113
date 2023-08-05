Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RepositorySwitcher = /** @class */ (function (_super) {
    tslib_1.__extends(RepositorySwitcher, _super);
    function RepositorySwitcher() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.dropdownButton = react_1.createRef();
        _this.handleRepoFilterChange = function (activeRepo) {
            var _a = _this.props, router = _a.router, location = _a.location;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, activeRepo: activeRepo }) }));
        };
        return _this;
    }
    RepositorySwitcher.prototype.componentDidMount = function () {
        this.setButtonDropDownWidth();
    };
    RepositorySwitcher.prototype.setButtonDropDownWidth = function () {
        var _a, _b;
        var dropdownButtonWidth = (_b = (_a = this.dropdownButton) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetWidth;
        if (dropdownButtonWidth) {
            this.setState({ dropdownButtonWidth: dropdownButtonWidth });
        }
    };
    RepositorySwitcher.prototype.render = function () {
        var _this = this;
        var _a = this.props, activeRepository = _a.activeRepository, repositories = _a.repositories;
        var dropdownButtonWidth = this.state.dropdownButtonWidth;
        var activeRepo = activeRepository === null || activeRepository === void 0 ? void 0 : activeRepository.name;
        return (<StyledDropdownControl minMenuWidth={dropdownButtonWidth} label={<react_1.Fragment>
            <FilterText>{locale_1.t('Filter') + ":"}</FilterText>
            {activeRepo}
          </react_1.Fragment>} buttonProps={{ forwardRef: this.dropdownButton }}>
        {repositories
                .map(function (repo) { return repo.name; })
                .map(function (repoName) { return (<dropdownControl_1.DropdownItem key={repoName} onSelect={_this.handleRepoFilterChange} eventKey={repoName} isActive={repoName === activeRepo}>
              <RepoLabel>{repoName}</RepoLabel>
            </dropdownControl_1.DropdownItem>); })}
      </StyledDropdownControl>);
    };
    return RepositorySwitcher;
}(react_1.PureComponent));
exports.default = RepositorySwitcher;
var StyledDropdownControl = styled_1.default(dropdownControl_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  > *:nth-child(2) {\n    right: auto;\n    width: auto;\n    ", "\n    border-radius: ", ";\n    border-top-left-radius: 0px;\n    border: 1px solid ", ";\n    top: calc(100% - 1px);\n  }\n"], ["\n  margin-bottom: ", ";\n  > *:nth-child(2) {\n    right: auto;\n    width: auto;\n    ", "\n    border-radius: ", ";\n    border-top-left-radius: 0px;\n    border: 1px solid ", ";\n    top: calc(100% - 1px);\n  }\n"])), space_1.default(1), function (p) { return p.minMenuWidth && "min-width: calc(" + p.minMenuWidth + "px + 10px);"; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.button.default.border; });
var FilterText = styled_1.default('em')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-style: normal;\n  color: ", ";\n  margin-right: ", ";\n"], ["\n  font-style: normal;\n  color: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.gray300; }, space_1.default(0.5));
var RepoLabel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=repositorySwitcher.jsx.map