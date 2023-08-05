Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var annotated_1 = tslib_1.__importDefault(require("app/components/events/meta/annotated"));
var locale_1 = require("app/locale");
var EventSdk = function (_a) {
    var sdk = _a.sdk;
    return (<eventDataSection_1.default type="sdk" title={locale_1.t('SDK')}>
    <table className="table key-value">
      <tbody>
        <tr key="name">
          <td className="key">{locale_1.t('Name')}</td>
          <td className="value">
            <annotated_1.default object={sdk} objectKey="name">
              {function (value) { return <pre className="val-string">{value}</pre>; }}
            </annotated_1.default>
          </td>
        </tr>
        <tr key="version">
          <td className="key">{locale_1.t('Version')}</td>
          <td className="value">
            <annotated_1.default object={sdk} objectKey="version">
              {function (value) { return <pre className="val-string">{value}</pre>; }}
            </annotated_1.default>
          </td>
        </tr>
      </tbody>
    </table>
  </eventDataSection_1.default>);
};
exports.default = EventSdk;
//# sourceMappingURL=eventSdk.jsx.map