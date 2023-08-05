Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var fileChange_1 = tslib_1.__importDefault(require("app/components/fileChange"));
var listGroup_1 = require("app/components/listGroup");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function Collapsed(props) {
    return (<listGroup_1.ListGroupItem centered>
      <a onClick={props.onClick}>
        {locale_1.tn('Show %s collapsed file', 'Show %s collapsed files', props.count)}
      </a>
    </listGroup_1.ListGroupItem>);
}
var RepositoryFileSummary = /** @class */ (function (_super) {
    tslib_1.__extends(RepositoryFileSummary, _super);
    function RepositoryFileSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            collapsed: true,
        };
        _this.onCollapseToggle = function () {
            _this.setState({
                collapsed: !_this.state.collapsed,
            });
        };
        return _this;
    }
    RepositoryFileSummary.prototype.render = function () {
        var _a = this.props, repository = _a.repository, fileChangeSummary = _a.fileChangeSummary, collapsable = _a.collapsable, maxWhenCollapsed = _a.maxWhenCollapsed;
        var files = Object.keys(fileChangeSummary);
        var fileCount = files.length;
        files.sort();
        if (this.state.collapsed && collapsable && fileCount > maxWhenCollapsed) {
            files = files.slice(0, maxWhenCollapsed);
        }
        var numCollapsed = fileCount - files.length;
        var canCollapse = collapsable && fileCount > maxWhenCollapsed;
        return (<Container>
        <h5>
          {locale_1.tn('%s file changed in ' + repository, '%s files changed in ' + repository, fileCount)}
        </h5>
        <listGroup_1.ListGroup striped>
          {files.map(function (filename) {
                var authors = fileChangeSummary[filename].authors;
                return (<fileChange_1.default key={filename} filename={filename} authors={authors ? Object.values(authors) : []}/>);
            })}
          {numCollapsed > 0 && (<Collapsed onClick={this.onCollapseToggle} count={numCollapsed}/>)}
          {numCollapsed === 0 && canCollapse && (<listGroup_1.ListGroupItem centered>
              <a onClick={this.onCollapseToggle}>{locale_1.t('Collapse')}</a>
            </listGroup_1.ListGroupItem>)}
        </listGroup_1.ListGroup>
      </Container>);
    };
    RepositoryFileSummary.defaultProps = {
        collapsable: true,
        maxWhenCollapsed: 5,
    };
    return RepositoryFileSummary;
}(React.Component));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
exports.default = RepositoryFileSummary;
var templateObject_1;
//# sourceMappingURL=repositoryFileSummary.jsx.map