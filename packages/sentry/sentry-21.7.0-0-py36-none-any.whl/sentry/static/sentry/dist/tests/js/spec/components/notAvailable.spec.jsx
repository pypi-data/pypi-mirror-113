Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
describe('NotAvailable', function () {
    it('renders', function () {
        var wrapper = enzyme_1.mountWithTheme(<notAvailable_1.default />);
        expect(wrapper.text()).toEqual('\u2014');
    });
    it('renders with tooltip', function () {
        var wrapper = enzyme_1.mountWithTheme(<notAvailable_1.default tooltip="Tooltip text"/>);
        expect(wrapper.text()).toEqual('\u2014');
        expect(wrapper.find('Tooltip').prop('title')).toBe('Tooltip text');
    });
});
//# sourceMappingURL=notAvailable.spec.jsx.map