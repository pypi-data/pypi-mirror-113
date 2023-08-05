Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var AdminWarnings = /** @class */ (function (_super) {
    tslib_1.__extends(AdminWarnings, _super);
    function AdminWarnings() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminWarnings.prototype.getEndpoints = function () {
        return [['data', '/internal/warnings/']];
    };
    AdminWarnings.prototype.renderBody = function () {
        var data = this.state.data;
        if (data === null) {
            return null;
        }
        var groups = data.groups, warnings = data.warnings;
        return (<div>
        <h3>{locale_1.t('System Warnings')}</h3>
        {!warnings && !groups && locale_1.t('There are no warnings at this time')}

        {groups.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), groupName = _b[0], groupedWarnings = _b[1];
                return (<react_1.Fragment key={groupName}>
            <h4>{groupName}</h4>
            <ul>
              {groupedWarnings.map(function (warning, i) { return (<li key={i}>{warning}</li>); })}
            </ul>
          </react_1.Fragment>);
            })}

        {warnings.length > 0 && (<react_1.Fragment>
            <h4>Miscellaneous</h4>
            <ul>
              {warnings.map(function (warning, i) { return (<li key={i}>{warning}</li>); })}
            </ul>
          </react_1.Fragment>)}
      </div>);
    };
    return AdminWarnings;
}(asyncView_1.default));
exports.default = AdminWarnings;
//# sourceMappingURL=adminWarnings.jsx.map